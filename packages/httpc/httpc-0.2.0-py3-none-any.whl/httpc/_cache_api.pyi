from typing import Callable
from collections import deque

from httpc._css import CSSResponse

from ._api import (
    request as crequest,
    get as cget,
    options as coptions,
    head as chead,
    post as cpost,
    put as cput,
    patch as cpatch,
    delete as cdelete,
)

__all__ = ["crequest", "cget", "coptions", "chead", "cpost", "cput", "cpatch", "cdelete"]
_caches: deque[tuple[Callable, tuple, dict, CSSResponse]] = deque([], maxlen=127)
