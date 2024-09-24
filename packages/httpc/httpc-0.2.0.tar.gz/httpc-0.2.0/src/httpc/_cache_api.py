from __future__ import annotations

import typing
from collections import deque

from . import _api as api

__all__ = ["crequest", "cget", "coptions", "chead", "cpost", "cput", "cpatch", "cdelete"]

# 시퀸스 대신 딕셔너리를 사용하면 키카 hashable해야 하고 심지어 (아마도) 더 느림.
# 이 방식을 이용하면 이론상 더 느리지만 캐시 API는 production에서
# 사용하기 위한 코드가 아니기 때문에 괜찮음
_caches: deque[tuple[typing.Any, typing.Any, typing.Any, typing.Any]] = deque([], maxlen=127)


def crequest(*args, **kwargs):
    for func, args_cache, kwargs_cache, value in _caches:
        if crequest is func and args == args_cache and kwargs == kwargs_cache:
            return value
    result = api.request(*args, **kwargs)
    _caches.append((crequest, args, kwargs, result))
    return result


def cget(*args, **kwargs):
    for func, args_cache, kwargs_cache, value in _caches:
        if cget is func and args == args_cache and kwargs == kwargs_cache:
            return value
    result = api.get(*args, **kwargs)
    _caches.append((cget, args, kwargs, result))
    return result


def coptions(*args, **kwargs):
    for func, args_cache, kwargs_cache, value in _caches:
        if coptions is func and args == args_cache and kwargs == kwargs_cache:
            return value
    result = api.options(*args, **kwargs)
    _caches.append((coptions, args, kwargs, result))
    return result


def chead(*args, **kwargs):
    for func, args_cache, kwargs_cache, value in _caches:
        if chead is func and args == args_cache and kwargs == kwargs_cache:
            return value
    result = api.head(*args, **kwargs)
    _caches.append((chead, args, kwargs, result))
    return result


def cpost(*args, **kwargs):
    for func, args_cache, kwargs_cache, value in _caches:
        if cpost is func and args == args_cache and kwargs == kwargs_cache:
            return value
    result = api.post(*args, **kwargs)
    _caches.append((cpost, args, kwargs, result))
    return result


def cput(*args, **kwargs):
    for func, args_cache, kwargs_cache, value in _caches:
        if cput is func and args == args_cache and kwargs == kwargs_cache:
            return value
    result = api.put(*args, **kwargs)
    _caches.append((cput, args, kwargs, result))
    return result


def cpatch(*args, **kwargs):
    for func, args_cache, kwargs_cache, value in _caches:
        if cpatch is func and args == args_cache and kwargs == kwargs_cache:
            return value
    result = api.patch(*args, **kwargs)
    _caches.append((cpatch, args, kwargs, result))
    return result


def cdelete(*args, **kwargs):
    for func, args_cache, kwargs_cache, value in _caches:
        if cdelete is func and args == args_cache and kwargs == kwargs_cache:
            return value
    result = api.delete(*args, **kwargs)
    _caches.append((cdelete, args, kwargs, result))
    return result
