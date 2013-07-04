# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging
import string
import random
from datetime import date
from sqlalchemy import func

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from pylons.decorators import jsonify

from guessword.model.meta import Session
from guessword.model.user import User
from guessword.model.training import Training

from guessword.lib.base import BaseController, render

log = logging.getLogger(__name__)

global Service
class Service(object):

    def user_exists(self, loginORemail, password):
        """Returns a user object and its training results if user with 
        specified login and password exists.

        :Parameters:
            login: (unicode) Lgin entered by tne user.
            password: (unicode) Password entered by tne user.
        :Return:
            (class, class) User object if user exists anf None otherwise.
        """
        # checking if user with specified login and password exists
        query = Session.query(User).\
        filter(((User.Login == loginORemail) | (User.Email == loginORemail)) \
            & (User.Password == password))

        return query.first()

    def calculate_user_age(self, DOB):
        """Returns age of the user.

        :Parameters:
            user_info: (class) User object.
        :Return:
            (int) Age of the user.
        """
        if DOB is not None:
            difference = date.today() - DOB
            age = difference.days//365
            return int(age)

    def pass_generator(self, size=6, chars=string.ascii_uppercase + string.digits):
        """Generates a password consisting of uppercase letters and digits.
        """
        return ''.join(random.choice(chars) for x in range(size))

    def email_exists(self, email):
        """Returns True if user with specified email already exists in DB.

        :Parameters:
            email: (unicode) An email provided by the user.
        :Return:
            (bool) True if email exists in DB and None otherwise.
        """
        email_exists = \
                Session.query(User).filter(User.Email == email).first()
        return email_exists
