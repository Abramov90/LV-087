# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from pylons.decorators import jsonify
from guessword.model.meta import Session
from guessword.model import User

from guessword.lib.base import BaseController, render

log = logging.getLogger(__name__)

class LoginController(BaseController):

    @jsonify
    def index(self):
        """Returns a JSON representation of user personl data, 
        if the user with indicated login and password exists"""
        # setting a response header to enable access control 
        # using cross-origin resource sharing
        response.headers['Access-Control-Allow-Origin'] = '*'

        # accepting data from a request
        log_info = {"login"   : (request.POST["userLogIn"]).encode('utf8'), 
                    "password": (request.POST["userPassword"]).encode('utf8')}

        # checking if user with specified login and password exists.
        user_info = Session.query(User.Login, User.Password, User.Email, User.DOB, User.Location).\
        filter(((User.Login == log_info["login"]) | (User.Email == log_info["login"])) & (User.Password == log_info["password"]))

        # responce
        json_user = {}

        # creating a JSON object
        attributes = ("login", "pass", "email", "dob", "location")
        if user_info.first():
            user_info = list(user_info.first())
            # turning date format into a string
            user_info[-2] = str(user_info[-2])
            # handling unicode representation of location data
            user_info[-1] = unicode(user_info[-1])
            for (num, attr) in enumerate(attributes):
                json_user[attr] = user_info[num]
        else:
            json_user["ANSWER"] = "User does not exist"
        
        return json_user