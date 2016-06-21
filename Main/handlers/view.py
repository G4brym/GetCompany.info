from .utilities import get_title
import json
from django.conf import settings

class view_handler():
    _dict = None
    _request = None

    def __init__(self, request, title):
        self._dict = {
            "title": None,
            "media_url": settings.MEDIA_URL,
            "input": {},
            "page_content": {},
            "success": None,
            "errors": {
                "form": {},
                "normal": [],
                "passed_by": None,
            }
        }

        self._dict["title"] = get_title(title)

        try:
            self._dict["success"] = request.session.get("success", None)
            if self._dict["success"] != None:
                del request.session["success"]
        except KeyError:
            self._dict["success"] = None

        try:
            self._dict["errors"]["passed_by"] = request.session.get("errors", None)
            if self._dict["errors"]["passed_by"] != None:
                del request.session["errors"]
        except KeyError:
            self._dict["errors"]["passed_by"] = None

        self._request = request

    def get_dict(self):
        return self._dict

    def get_request(self):
        return self._request

def add_success(request, success):
    request.session["success"] = success
    return request

def add_error(request, error):
    request.session["errors"] = error
    return request
