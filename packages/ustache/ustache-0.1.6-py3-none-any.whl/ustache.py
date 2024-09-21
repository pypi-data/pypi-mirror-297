"""
ustache module.

This module is a deprecated backwards-compatible wrapper based on
:mod:`mustache` to simplify the migration and provide fixes.

.. deprecated:: 0.1.6
    Developers should migrate to :mod:`mstache`.

"""
"""
ustache, mstache wrapper, Mustache for Python
=============================================

This project has been renamed to **mstache**, refer to the new
`mstache README.md`_ and `mstache repository`_.

See also `README.md`_, `project documentation`_ and `project repository`_.

.. _mstache README.md: https://mstache.readthedocs.io/en/latest/README.html
.. _mstache repository: https://gitlab.com/ergoithz/mstache
.. _README.md: https://ustache.readthedocs.io/en/latest/README.html
.. _project documentation: https://ustache.readthedocs.io
.. _project repository: https://gitlab.com/ergoithz/ustache


License
-------

Copyright (c) 2021-2024, Felipe A Hernandez.

MIT License (see `LICENSE`_).

.. _LICENSE: https://gitlab.com/ergoithz/ustache/-/blob/master/LICENSE

"""

import collections
import collections.abc
import sys
import typing

import mstache
from mstache import (
    ClosingTokenException,
    CompiledTemplate,
    CompiledTemplateCache,
    CompiledToken,
    DelimiterTokenException,
    EscapeFunction,
    LambdaRenderFunctionConstructor,
    LambdaRenderFunctionFactory,
    PartialResolver,
    PropertyGetter,
    StringifyFunction,
    TString,
    TagsTuple,
    TokenException,
    UnclosedTokenException,
    cli,
    default_cache,
    default_escape,
    default_getter,
    default_lambda_render,
    default_resolver,
    default_stringify,
    default_tags,
    default_virtuals,
    )

try:
    import xxhash  # type: ignore
    _cache_hash = getattr(xxhash, 'xxh3_64_intdigest', xxhash.xxh64_intdigest)

    def _cache_make_key(
            params: tuple[bytes, bytes, bytes, bool], /,
            ) -> tuple[int, bytes, bytes, bool]:
        """
        Generate template hash using the fastest algorithm available.

        :param params: tuple of tokenization params
        :returns: integer hash

        Implementation
        --------------

        1. :py:func:`xxhash.xxh3_64_intdigest` from ``python-xxhash>=2.0.0``.
        2. :py:func:`xxhash.xxh64_intdigest` from ``python-xxhash>=1.2.0``.

        """
        template, start, end, comments = params
        return _cache_hash(template), start, end, comments

except (ImportError, AttributeError):
    _cache_make_key = mstache.default_cache_make_key

__author__ = 'Felipe A Hernandez'
__email__ = 'ergoithz@gmail.com'
__license__ = 'MIT'
__version__ = '0.1.6'
__all__ = (
    # api
    'tokenize',
    'stream',
    'render',
    'cli',
    # exceptions
    'TokenException',
    'ClosingTokenException',
    'UnclosedTokenException',
    'DelimiterTokenException',
    # defaults
    'default_resolver',
    'default_getter',
    'default_stringify',
    'default_escape',
    'default_lambda_render',
    'default_tags',
    'default_cache',
    'default_virtuals',
    # types
    'TString',
    'PartialResolver',
    'PropertyGetter',
    'StringifyFunction',
    'EscapeFunction',
    'LambdaRenderFunctionFactory',
    'LambdaRenderFunctionConstructor',
    'CompiledTemplate',
    'CompiledToken',
    'CompiledTemplateCache',
    'TagsTuple',
    )

T = typing.TypeVar('T')
"""Generic."""

_disable_recursion_limit = sys.maxsize


def replay(
        recording: collections.abc.Sequence[T],
        start: int = 0,
        ) -> collections.abc.Generator[T, int, None]:
    """
    Yield sequence, rewinding it to any index being sent.

    This generator accepts sending back a token index, which will result on
    rewinding it back and repeat everything from there.

    :param sequence: item sequence
    :param start: starting index
    :returns: token tuple generator

    """
    size = len(recording)
    while True:
        for item in range(start, size):
            start = yield recording[item]
            if start is not None:
                break
        else:
            break


def tokenize(
        template: bytes,
        *,
        tags: TagsTuple = default_tags,
        comments: bool = False,
        cache: CompiledTemplateCache = default_cache,
        ) -> collections.abc.Generator[CompiledToken, int, None]:
    """
    Generate token tuples from mustache template.

    This generator accepts sending back a token index, which will result on
    rewinding it back and repeat everything from there.

    Starting from **v0.1.6** this is just a rewindable generator proxy for
    :func:`mstache.tokenize`.

    :param template: template as utf-8 encoded bytes
    :param tags: mustache tag tuple (open, close)
    :param comments: whether yield comment tokens or not (ignore comments)
    :param cache: mutable mapping for compiled template cache
    :return: token tuple generator (type, name slice, content slice, option)

    :raises UnclosedTokenException: if token is left unclosed
    :raises ClosingTokenException: if block closing token does not match
    :raises DelimiterTokenException: if delimiter token syntax is invalid

    """
    return replay(mstache.tokenize(
        template=template,
        tags=tags,
        comments=comments,
        cache=cache,
        ))


def process(
        template: TString,
        scope: typing.Any,
        *,
        scopes: collections.abc.Iterable = (),
        resolver: PartialResolver = default_resolver,
        getter: PropertyGetter = default_getter,
        stringify: StringifyFunction = default_stringify,
        escape: EscapeFunction = default_escape,
        lambda_render: LambdaRenderFunctionConstructor = default_lambda_render,
        tags: TagsTuple = default_tags,
        cache: CompiledTemplateCache = default_cache,
        ) -> collections.abc.Generator[bytes, None, None]:
    """
    Generate rendered mustache template byte chunks.

    Starting from **v0.1.6** this is just a proxy for :func:`mstache.process`.

    :param template: mustache template string
    :param scope: root object used as root mustache scope
    :param scopes: iterable of parent scopes
    :param resolver: callable will be used to resolve partials (bytes)
    :param getter: callable will be used to pick variables from scope
    :param stringify: callable will be used to render python types (bytes)
    :param escape: callable will be used to escape template (bytes)
    :param lambda_render: lambda render function constructor
    :param tags: mustache tag tuple (open, close)
    :param cache: mutable mapping for compiled template cache
    :return: byte chunk generator

    :raises UnclosedTokenException: if token is left unclosed
    :raises ClosingTokenException: if block closing token does not match
    :raises DelimiterTokenException: if delimiter token syntax is invalid

    """
    return mstache.process(
        template=template,
        scope=scope,
        scopes=scopes,
        resolver=resolver,
        getter=getter,
        stringify=stringify,
        escape=escape,
        lambda_render=lambda_render,
        tags=tags,
        cache=cache,
        cache_make_key=_cache_make_key,
        recursion_limit=_disable_recursion_limit,
        )


def stream(
        template: TString,
        scope: typing.Any,
        *,
        scopes: collections.abc.Iterable = (),
        resolver: PartialResolver = default_resolver,
        getter: PropertyGetter = default_getter,
        stringify: StringifyFunction = default_stringify,
        escape: EscapeFunction = default_escape,
        lambda_render: LambdaRenderFunctionConstructor = default_lambda_render,
        tags: TagsTuple = default_tags,
        cache: CompiledTemplateCache = default_cache,
        ) -> collections.abc.Generator[TString, None, None]:
    """
    Generate rendered mustache template chunks.

    Starting from **v0.1.6** this is just a proxy for :func:`mstache.stream`.

    :param template: mustache template (str or bytes)
    :param scope: current rendering scope (data object)
    :param scopes: list of precedent scopes
    :param resolver: callable will be used to resolve partials (bytes)
    :param getter: callable will be used to pick variables from scope
    :param stringify: callable will be used to render python types (bytes)
    :param escape: callable will be used to escape template (bytes)
    :param lambda_render: lambda render function constructor
    :param tags: tuple (start, end) specifying the initial mustache delimiters
    :param cache: mutable mapping for compiled template cache
    :returns: generator of bytes/str chunks (same type as template)

    :raises UnclosedTokenException: if token is left unclosed
    :raises ClosingTokenException: if block closing token does not match
    :raises DelimiterTokenException: if delimiter token syntax is invalid
    :raises RenderingRecursionError: if rendering recursion limit is exceeded

    """
    return mstache.stream(
        template=template,
        scope=scope,
        scopes=scopes,
        resolver=resolver,
        getter=getter,
        stringify=stringify,
        escape=escape,
        lambda_render=lambda_render,
        tags=tags,
        cache=cache,
        cache_make_key=_cache_make_key,
        recursion_limit=_disable_recursion_limit,
        )


def render(
        template: TString,
        scope: typing.Any,
        *,
        scopes: collections.abc.Iterable = (),
        resolver: PartialResolver = default_resolver,
        getter: PropertyGetter = default_getter,
        stringify: StringifyFunction = default_stringify,
        escape: EscapeFunction = default_escape,
        lambda_render: LambdaRenderFunctionConstructor = default_lambda_render,
        tags: TagsTuple = default_tags,
        cache: CompiledTemplateCache = default_cache,
        ) -> TString:
    """
    Render mustache template.

    Starting from **v0.1.6** this is just a proxy for :func:`mstache.render`.

    :param template: mustache template
    :param scope: current rendering scope (data object)
    :param scopes: list of precedent scopes
    :param resolver: callable will be used to resolve partials (bytes)
    :param getter: callable will be used to pick variables from scope
    :param stringify: callable will be used to render python types (bytes)
    :param escape: callable will be used to escape template (bytes)
    :param lambda_render: lambda render function constructor
    :param tags: tuple (start, end) specifying the initial mustache delimiters
    :param cache: mutable mapping for compiled template cache
    :returns: rendered bytes/str (type depends on template)

    :raises UnclosedTokenException: if token is left unclosed
    :raises ClosingTokenException: if block closing token does not match
    :raises DelimiterTokenException: if delimiter token syntax is invalid

    """
    return mstache.render(
        template=template,
        scope=scope,
        scopes=scopes,
        resolver=resolver,
        getter=getter,
        stringify=stringify,
        escape=escape,
        lambda_render=lambda_render,
        tags=tags,
        cache=cache,
        cache_make_key=_cache_make_key,
        recursion_limit=_disable_recursion_limit,
        )


if __name__ == '__main__':
    cli()
