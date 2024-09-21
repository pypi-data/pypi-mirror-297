# Flask URL Patterns

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