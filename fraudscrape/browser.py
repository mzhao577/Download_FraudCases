"""Headless-Chrome layer.

Two jobs:

1. Fetch pages that plain HTTP clients cannot get (justice.gov, cms.gov and
   gao.gov all sit behind bot-management walls that require real JS execution).
2. Turn HTML into PDF, which is what the instructions ask for whenever a report
   is only published as a web page.

One Chrome per worker thread, created lazily and recycled if it dies.
"""

from __future__ import annotations

import atexit
import base64
import logging
import threading
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.print_page_options import PrintOptions

from . import config

log = logging.getLogger(__name__)

_local = threading.local()
_all_drivers: list = []
_drivers_lock = threading.Lock()

PAGE_LOAD_TIMEOUT = 75
SETTLE_SECONDS = 1.5          # let late JS (and bot-wall redirects) finish


def _make_options() -> Options:
    o = Options()
    o.add_argument("--headless=new")
    o.add_argument("--disable-gpu")
    o.add_argument("--no-first-run")
    o.add_argument("--no-default-browser-check")
    o.add_argument("--disable-background-networking")
    o.add_argument("--disable-dev-shm-usage")
    o.add_argument("--hide-scrollbars")
    o.add_argument("--window-size=1280,1696")
    o.add_argument("--allow-file-access-from-files")
    o.add_argument(f"--user-agent={config.USER_AGENT}")
    o.add_experimental_option("excludeSwitches", ["enable-automation"])
    o.set_capability("pageLoadStrategy", "normal")
    return o


# A single Chrome slowly accumulates memory across thousands of page loads, so
# each worker restarts its browser periodically during a multi-hour run.
PAGES_PER_BROWSER = 300


def driver():
    d = getattr(_local, "driver", None)
    if d is not None:
        _local.uses = getattr(_local, "uses", 0) + 1
        if _local.uses < PAGES_PER_BROWSER:
            return d
        log.debug("recycling Chrome after %s uses", _local.uses)
        recycle()
        d = None
    _local.uses = 0
    d = webdriver.Chrome(options=_make_options())
    d.set_page_load_timeout(PAGE_LOAD_TIMEOUT)
    d.set_script_timeout(45)
    _local.driver = d
    with _drivers_lock:
        _all_drivers.append(d)
    return d


def recycle() -> None:
    """Throw away this thread's Chrome (used after a hard failure)."""
    d = getattr(_local, "driver", None)
    _local.driver = None
    if d is None:
        return
    with _drivers_lock:
        if d in _all_drivers:
            _all_drivers.remove(d)
    try:
        d.quit()
    except Exception:  # noqa: BLE001
        pass


def shutdown() -> None:
    with _drivers_lock:
        drivers, _all_drivers[:] = list(_all_drivers), []
    for d in drivers:
        try:
            d.quit()
        except Exception:  # noqa: BLE001
            pass


atexit.register(shutdown)


_print_opts = PrintOptions()
_print_opts.background = True
_print_opts.scale = 1.0
_print_opts.margin_top = 0.4
_print_opts.margin_bottom = 0.4
_print_opts.margin_left = 0.4
_print_opts.margin_right = 0.4


def _pdf_of_current_page(d) -> bytes | None:
    try:
        return base64.b64decode(d.print_page(_print_opts))
    except Exception as exc:  # noqa: BLE001
        log.debug("print_page failed: %r", exc)
        return None


def open_page(url: str, settle: float = SETTLE_SECONDS, retries: int = 2):
    """Load `url`; return (html, title) or (None, None)."""
    for attempt in range(retries + 1):
        d = driver()
        try:
            d.get(url)
            time.sleep(settle)
            html = d.page_source
            if html and len(html) > 1500 and "bm-verify" not in html[:4000]:
                return html, d.title
            # bot wall still up - give it one more beat, it self-redirects
            time.sleep(3.0)
            html = d.page_source
            if html and len(html) > 1500:
                return html, d.title
        except Exception as exc:  # noqa: BLE001
            log.debug("browser get failed (%s/%s) %s: %r", attempt + 1, retries + 1, url, exc)
            recycle()
            time.sleep(1.5 * (attempt + 1))
    return None, None


def fetch_html_and_pdf(url: str) -> tuple[str | None, bytes | None]:
    """Load a live URL once and return both its rendered HTML and a PDF of it."""
    html, _ = open_page(url)
    if html is None:
        return None, None
    return html, _pdf_of_current_page(driver())


def pdf_from_file(path, settle: float = 1.2) -> bytes | None:
    """Render a locally saved HTML file to PDF."""
    d = driver()
    try:
        d.get(f"file://{path}")
        time.sleep(settle)
        return _pdf_of_current_page(d)
    except Exception as exc:  # noqa: BLE001
        log.debug("pdf_from_file failed %s: %r", path, exc)
        recycle()
        return None


_FETCH_JS = """
const url = arguments[0];
const done = arguments[arguments.length - 1];
fetch(url, {credentials: 'include'}).then(function (r) {
  if (!r.ok) { done({error: 'HTTP ' + r.status}); return; }
  return r.arrayBuffer().then(function (buf) {
    const bytes = new Uint8Array(buf);
    if (bytes.length > 60000000) { done({error: 'too large'}); return; }
    let bin = '';
    const chunk = 0x8000;
    for (let i = 0; i < bytes.length; i += chunk) {
      bin += String.fromCharCode.apply(null, bytes.subarray(i, i + chunk));
    }
    done({data: btoa(bin)});
  });
}).catch(function (e) { done({error: String(e)}); });
"""


def fetch_binary(url: str, referer: str | None = None) -> bytes | None:
    """Pull a binary file through the browser (same-origin, keeps bot cookies).

    Used for PDFs on hosts that answer a bot wall to plain HTTP clients.
    """
    d = driver()
    try:
        origin = "/".join(url.split("/")[:3])
        landing = referer or origin
        if not (d.current_url or "").startswith(origin):
            d.get(landing)
            time.sleep(1.0)
        res = d.execute_async_script(_FETCH_JS, url)
    except Exception as exc:  # noqa: BLE001
        log.debug("browser fetch_binary failed %s: %r", url, exc)
        recycle()
        return None
    if not isinstance(res, dict) or not res.get("data"):
        log.debug("browser fetch_binary no data %s: %s", url, (res or {}).get("error"))
        return None
    try:
        return base64.b64decode(res["data"])
    except Exception:  # noqa: BLE001
        return None


def available() -> bool:
    """True when a headless Chrome can actually be started."""
    try:
        driver()
        return True
    except Exception as exc:  # noqa: BLE001
        log.warning("headless Chrome unavailable: %r", exc)
        return False
