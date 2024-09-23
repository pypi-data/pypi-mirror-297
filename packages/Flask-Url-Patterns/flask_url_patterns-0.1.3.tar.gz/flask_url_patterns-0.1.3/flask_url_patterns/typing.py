from __future__ import annotations

from abc import ABCMeta, abstractmethod
from collections.abc import Iterable
from typing import TYPE_CHECKING, Any, NotRequired, TypedDict

if TYPE_CHECKING:
    from flask import Flask
    from flask.typing import RouteCallable


class FlaskExtension(metaclass=ABCMeta):
    @abstractmethod
    def init_app(self, app: Flask, *args: Any, **kwargs: Any) -> None: ...


class URLPattern(TypedDict):
    """
    A URL pattern.
    """

    path: str | Iterable[str]
    name: NotRequired[str]
    view: NotRequired[RouteCallable]
    children: NotRequired[Iterable[URLPattern]]
    options: NotRequired[dict[str, Any]]
    parent_vars_rename: NotRequired[dict[str, str]]
