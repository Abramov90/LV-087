# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging
from datetime import date
from sqlalchemy import func

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from pylons.decorators import jsonify

from guessword.model.meta import Session
from guessword.model.user import User
from guessword.model.training import Training
from guessword.service.login_service import Service

from guessword.lib.base import BaseController, render

log = logging.getLogger(__name__)

class LoginController(BaseController, Service):

    @jsonify
    def index(self):
        """Returns a JSON representation of user personl data, 
        if the user with indicated login and password exists"""
        # setting a response header to enable access control 
        # using cross-origin resource sharing
        response.headers['Access-Control-Allow-Origin'] = '*'

        # accepting data from a request
        login = (request.POST["userLogIn"]).encode('utf8')
        password = (request.POST["userPassword"]).encode('utf8')

        # creating a JSON object with user info if such user exists
        try:
            user = self.user_exists(login, password)
            json_user = User.create_JSON_user(user, self.calculate_user_age(user.DOB))
            return json_user
        except (AttributeError, TypeError):
            return {}

    @jsonify
    def facebook(self):
        """Returns a JSON representation of user personal data, 
        if the user with indicated email and facebookID exists,
        otherwise registeres the user"""
        # setting a response header to enable access control 
        # using cross-origin resource sharing
        response.headers['Access-Control-Allow-Origin'] = '*'

        # accepting data from a request
        login = request.POST['login'], 
        email = request.POST['email'], 
        facebookID = request.POST['facebookID'], 
        DOB = request.POST['dob'], 
        location = request.POST['location']
        
        # creating a JSON object with user info if such user exists
        try:
            user = self.email_exists(email)
            User.add_facebookID(user, facebookID)
            Session.update(user)
            Session.commit()
            json_user = User.create_JSON_user(user, self.calculate_user_age(user.DOB))
            return json_user
        except (AttributeError, TypeError):
            # creating a new user
            new_user = User(login, self.pass_generator(), email, DOB, location, facebookID)
            Session.add(new_user)
            Session.commit()
            # creating a JSON object with user info
            json_user = User.create_JSON_user(new_user, self.calculate_user_age(new_user.DOB))
            return json_user