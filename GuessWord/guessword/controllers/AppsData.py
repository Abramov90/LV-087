import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from pylons.decorators import jsonify
from guessword.model.meta import Session
from guessword.model import AppsData

from guessword.lib.base import BaseController, render

log = logging.getLogger(__name__)

class AppsdataController(BaseController):

    @jsonify
    def index(self):
        """Returns a JSON representation of the table data"""
        json_apps = []
        for app in Session.query(AppsData):
            json_apps.append({
                "id": app.ID,
                "name": app.Name,
                "label": app.Label
                })

        return json_apps
