from __future__ import annotations

"""
This module provides functionality to manage URL patterns in a Flask application.

Classes:
    UrlPatterns: A Flask extension to manage URL patterns.

Functions:
    concat_paths(prefix: str, path: str) -> str:
        Concatenates two URL paths, ensuring there is exactly one '/' between them.

    gen_rules(
        Generates URL rules from the given URL patterns.

Usage:
    This module is intended to be used as a Flask extension to manage URL patterns
    in a structured way. The `UrlPatterns` class can be initialized with a Flask app
    and a list of URL patterns, and it will automatically add the URL rules to the app.
"""

import re
from collections.abc import Generator, Iterable
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from flask import Flask
    from flask.typing import RouteCallable

from .typing import FlaskExtension, URLPattern


def concat_paths(prefix: str, path: str) -> str:
    """
    Concatenates two URL paths, ensuring there is exactly one '/' between them.

    Args:
        prefix (str): The prefix path.
        path (str): The path to concatenate.

    Returns:
        concatenated_path (str): The concatenated path.
    """

    if prefix.endswith("/") and path.startswith("/"):
        return prefix[:-1] + path
    if not prefix.endswith("/") and not path.startswith("/"):
        return prefix + "/" + path
    return prefix + path


def gen_rules(
    urlpatterns: Iterable[URLPattern],
    prefix: str = "",
) -> Generator[tuple[str, RouteCallable, dict[str, Any]], None, None]:
    """
    Generates URL rules from the given URL patterns.

    Args:
        urlpatterns (Iterable[URLPattern]): The URL patterns to generate rules from.
        prefix (str): The prefix to prepend to the paths in the URL patterns.

    Yields:
        rule (tuple[str, RouteCallable, dict[str, Any]]): A tuple containing the URL rule, view function, and options.
    """

    for urlpattern in urlpatterns:
        for old_name, new_name in urlpattern.get("parent_vars_rename", {}).items():
            pattern = re.compile(f"(?<=[<:]){old_name}(?=>)")
            prefix = re.sub(pattern, new_name, prefix, count=1)
        paths = (
            [urlpattern["path"]]
            if isinstance(urlpattern["path"], str)
            else urlpattern["path"]
        )
        for path in paths:
            path = concat_paths(prefix, path)
            options = urlpattern.get("options", {})
            if "name" in urlpattern:
                options["endpoint"] = urlpattern["name"]
            if "view" in urlpattern:
                yield path, urlpattern["view"], options
            if "children" in urlpattern:
                yield from gen_rules(urlpattern["children"], path)


class UrlPatterns(FlaskExtension):
    """
    A Flask extension to manage URL patterns.

    Attributes:
        app (Flask): The Flask app to which the URL patterns are added.
        urlpatterns (Iterable[URLPattern]): The routing configuration.
    """

    def __init__(
        self,
        app: Flask | None = None,
        urlpatterns: Iterable[URLPattern] | None = None,
    ) -> None:
        """
        Initializes the extension with the given Flask app and URL patterns.

        Args:
            app (Flask | None): The Flask app to which the URL patterns are added.
            urlpatterns (Iterable[URLPattern] | None): The routing configuration.
        """
        self.urlpatterns = urlpatterns
        if app is not None:
            self.init_app(app)

    def init_app(
        self,
        app: Flask,
        urlpatterns: Iterable[URLPattern] | None = None,
    ) -> None:
        """
        Initializes the extension with the given Flask app and URL patterns.

        Args:
            app (Flask): The Flask app to which the URL patterns are added.
            urlpatterns (Iterable[URLPattern] | None): The routing configuration.
        """
        self.app = app
        self.urlpatterns = urlpatterns or self.urlpatterns
        assert self.urlpatterns is not None, "URL patterns are not defined"
        for rule, view, options in gen_rules(self.urlpatterns):
            self.app.add_url_rule(rule, view_func=view, **options)
        self.app.extensions["url_patterns"] = self
