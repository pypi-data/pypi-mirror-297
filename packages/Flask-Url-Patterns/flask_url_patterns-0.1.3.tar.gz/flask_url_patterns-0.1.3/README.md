# Flask URL Patterns

## Usage

You must instanciate UrlPatterns and provide the urlpatterns param to it as well as a Flask app instance either in \_\_init\_\_ or init_app params.

`urlpatterns` must be of type: `Iterable[URLPattern]` with:

```python
class URLPattern(TypedDict):
    path: str | Iterable[str]
    name: NotRequired[str]
    view: NotRequired[RouteCallable]
    children: NotRequired[Iterable[URLPattern]]
    options: NotRequired[dict[str, Any]]
    parent_vars_rename: NotRequired[dict[str, str]]
```

_(In case typing is not up to date in README.md, know that you can see current accepted typing in `flask_url_patterns.typing`)_

## Example

```python
from flask import Flask
from flask_url_patterns import URLPatterns

from . import views

app = Flask(__name__)

urlpatterns = UrlPatterns(urlpatterns=[
    {
        "path": "/",
        "name": "index",
        "view": views.index,
        "children": [
            {
                "path": "/api",
                "name": "api",
                "children": [
                    {
                        "path": "/resources",
                        "view": views.ResourceViewSet.as_view({ # Using as implemented by [Flask-ViewSets](https://pypi.org/project/Flask-Viewsets/)
                            "get": "list",
                            "post": "create",
                        }),
                        "children": [
                            {
                                "path": "/<int:id>",
                                "view": views.ResourceViewSet.as_view({
                                    "get": "retrieve",
                                    "put": "update",
                                    "patch": "partial_update",
                                    "delete": "destroy",
                                }),
                            },
                        ],
                    },
                ]
            },
        ],
    },
])

urlpatterns.init_app(app)
```
