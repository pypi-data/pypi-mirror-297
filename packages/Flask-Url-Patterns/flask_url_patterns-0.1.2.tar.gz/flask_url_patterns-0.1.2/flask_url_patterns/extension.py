from __future__ import annotations

from collections.abc import Generator, Iterable
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from flask import Flask
    from flask.typing import RouteCallable

from .typing import FlaskExtension, URLPattern


def concat_paths(prefix: str, path: str) -> str:
    if prefix.endswith("/") and path.startswith("/"):
        return prefix[:-1] + path
    if not prefix.endswith("/") and not path.startswith("/"):
        return prefix + "/" + path
    return prefix + path


def gen_rules(
    urlpatterns: Iterable[URLPattern],
    prefix: str = "",
) -> Generator[tuple[str, RouteCallable, dict[str, Any]], None, None]:
    for urlpattern in urlpatterns:
        path = concat_paths(prefix, urlpattern["path"])
        options = urlpattern.get("options", {})
        if "name" in urlpattern:
            options["endpoint"] = urlpattern["name"]
        if "view" in urlpattern:
            yield path, urlpattern["view"], options
        if "children" in urlpattern:
            yield from gen_rules(urlpattern["children"], path)


class UrlPatterns(FlaskExtension):
    def __init__(
        self,
        app: Flask | None = None,
        urlpatterns: Iterable[URLPattern] | None = None,
    ) -> None:
        self.urlpatterns = urlpatterns
        if app is not None:
            self.init_app(app)

    def init_app(
        self,
        app: Flask,
        urlpatterns: Iterable[URLPattern] | None = None,
    ) -> None:
        self.app = app
        self.urlpatterns = urlpatterns or self.urlpatterns
        assert self.urlpatterns is not None, "URL patterns are not defined"
        for rule, view, options in gen_rules(self.urlpatterns):
            self.app.add_url_rule(rule, view_func=view, **options)
        self.app.extensions["url_patterns"] = self
