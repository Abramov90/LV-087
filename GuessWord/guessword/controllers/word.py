import logging, simplejson


from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from guessword.lib.base import BaseController, render

log = logging.getLogger(__name__)

class WordController(BaseController):

    def index(self):
        # Return a rendered template
        #return render('/word.mako')
        # or, return a string
        c.teamname = 'LV-087'
        return render('/custompage.html')
        
    def json(self):
        json_apps = '{apps: [app1, app2, app3], ss: 7}'
        response.headers['Content-type'] = 'application/json'
        return simplejson.dumps(json_apps, sort_keys=True, indent=4 * ' ')
