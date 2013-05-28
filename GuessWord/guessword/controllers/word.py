import logging

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
