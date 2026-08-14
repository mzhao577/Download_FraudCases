"""Plain-HTTP fetching: shared session, retries, per-host rate limiting."""

from __future__ import annotations

import logging
import threading
import time
from urllib.parse import urlparse

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from . import config

log = logging.getLogger(__name__)

_local = threading.local()
_host_lock = threading.Lock()
_last_hit: dict[str, float] = {}

# Markers that mean "we got a bot wall, not the document".
BLOCK_MARKERS = (b"bm-verify", b"Access Denied", b"Request unsuccessful", b"_sec/verify")


def session() -> requests.Session:
    s = getattr(_local, "session", None)
    if s is None:
        s = requests.Session()
        s.headers.update(
            {
                "User-Agent": config.USER_AGENT,
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.9",
                "Connection": "keep-alive",
            }
        )
        retry = Retry(
            total=3,
            backoff_factor=1.2,
            status_forcelist=(429, 500, 502, 503, 504),
            allowed_methods=frozenset(["GET", "HEAD"]),
            respect_retry_after_header=True,
        )
        adapter = HTTPAdapter(max_retries=retry, pool_maxsize=32, pool_connections=32)
        s.mount("https://", adapter)
        s.mount("http://", adapter)
        _local.session = s
    return s


def throttle(url: str) -> None:
    host = urlparse(url).netloc
    delay = config.HOST_DELAY.get(host, config.DEFAULT_HOST_DELAY)
    with _host_lock:
        prev = _last_hit.get(host, 0.0)
        wait = delay - (time.monotonic() - prev)
        if wait > 0:
            time.sleep(wait)
        _last_hit[host] = time.monotonic()


def get(url: str, *, timeout: int = 60, rate_limit: bool = True, **kw) -> requests.Response:
    if rate_limit:
        throttle(url)
    return session().get(url, timeout=timeout, **kw)


def looks_blocked(resp: requests.Response) -> bool:
    if resp.status_code in (403, 406, 429) or resp.status_code >= 500:
        return True
    body = resp.content or b""
    if len(body) < 4000 and any(m in body for m in BLOCK_MARKERS):
        return True
    return any(m in body[:4000] for m in BLOCK_MARKERS)


def get_text(url: str, *, timeout: int = 60) -> str | None:
    """GET and return decoded text, or None on failure / bot wall."""
    try:
        r = get(url, timeout=timeout)
    except Exception as exc:  # noqa: BLE001
        log.debug("GET failed %s: %r", url, exc)
        return None
    if r.status_code != 200 or looks_blocked(r):
        log.debug("GET blocked/bad %s: %s", url, r.status_code)
        return None
    return r.text


def get_bytes(url: str, *, timeout: int = 120) -> bytes | None:
    try:
        r = get(url, timeout=timeout)
    except Exception as exc:  # noqa: BLE001
        log.debug("GET failed %s: %r", url, exc)
        return None
    if r.status_code != 200 or looks_blocked(r):
        return None
    return r.content
