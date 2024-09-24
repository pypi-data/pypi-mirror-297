from __future__ import annotations

import typing

from selectolax.parser import HTMLParser, Node, Selector
from httpx._models import Response

from ._broadcaster import BroadcastList

if typing.TYPE_CHECKING:
    from ._broadcaster import NodeBroadcastList

__all__ = ["CSSTool", "CSSResponse"]

T = typing.TypeVar("T")
_ABSENT = object()


class CSSTool:
    __slots__ = "text", "_cache"

    def __init__(self, text: str | None) -> None:
        if text is not None:
            self.text: str = text

    def parse(self, refresh: bool = False) -> HTMLParser:
        if refresh:
            self._cache = HTMLParser(self.text)
            return self._cache
        try:
            return self._cache
        except AttributeError:
            self._cache = HTMLParser(self.text)
            return self._cache

    def select(self, query: str) -> Selector:
        result = self.parse().select(query)
        if result is None:
            raise ValueError(f"{self} does not have root node.")
        return result

    def css(self, query: str) -> NodeBroadcastList:
        return BroadcastList(self.parse().css(query))  # type: ignore

    @typing.overload
    def single(self, query: str, *, remain_ok: bool = False) -> Node: ...

    @typing.overload
    def single(self, query: str, default: T, *, remain_ok: bool = False) -> Node | T: ...

    def single(self, query, default=_ABSENT, *, remain_ok=False):
        css_result = self.parse().css(query)
        length = len(css_result)

        if length == 0:
            if default is _ABSENT:
                raise ValueError(f"Query {query!r} matched with no nodes.")
            else:
                return default
        elif remain_ok or length == 1:
            return css_result.pop()
        else:
            raise ValueError(f"Query {query!r} matched with {length} nodes.")


class CSSResponse(Response, CSSTool):
    def __init__(self, response: Response) -> None:
        self.__dict__ = response.__dict__
