"""Per-source discovery modules.

Every module exposes `discover(since, limit=None, **kw) -> list[Doc]`.
The key used here must match the "key" in sources.json and is also the folder
name used under ./downloaded/.
"""

from . import cms, doj, fbi, gao, hhs_oig

REGISTRY = {
    "DOJ": doj.discover,
    "HHS-OIG": hhs_oig.discover,
    "FBI": fbi.discover,
    "CMS": cms.discover,
    "GAO": gao.discover,
}

__all__ = ["REGISTRY"]
