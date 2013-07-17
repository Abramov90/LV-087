# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging

from pylons.decorators import jsonify
from guessword.model.meta import Session
from guessword.model.user import User
from guessword.model.training import Training
import re

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from guessword.lib.base import BaseController, render

log = logging.getLogger(__name__)

class RegistrationController(BaseController):

    def __email_check(self, email):
        """
        Returns True if user with specified email already exists in DB.

        :Parameters:
            email: (unicode) An email provided by the user.
        :Return:
            (bool) True if email exists in DB and False otherwise.
        """
        email_exists = \
                Session.query(User.Email).filter(User.Email == email).count()
        if email_exists:
            return True

    def __login_check(self, login):
        """
        Returns True if user with specified login already exists in DB.

        :Parameters:
            login: (unicode) A login provided by the user.
        :Return:
            (bool) True if login exists in DB and False otherwise.
        """
        login_exists = \
                Session.query(User.Login).filter(User.Login == login).count()
        if login_exists:
            return True

    def __validate_registration(self, reg_info):
        """
        Returns success message if user entered data in a required 
        format and unique login and email 
        Otherwise returns a list of errors.

        :Parameters:
            reg_info: (dict of str: unicode) Information about the user.
        :Return:
            (list of str) A list of errors found.
        """
        # objects needed to be checked
        validate =  {'login': self.__login_check,
                     'email': self.__email_check}

        # answer to be created                     
        answer = {}

        # validation
        for field in ("login", "email"):
            if validate[field](reg_info[field]):
                answer[field] = "app_back_" + field

        # appending success message if no errors found
        if answer == {}:
            answer["SUCCESS"] = 1
        else:
            response.status = 405

        return answer

    @jsonify
    def index(self):
        """
        Adds a new user to the user table if another user
        with the same login does not exist.
        """
        # Setting a response header to enable access control
        # using cross-origin resource sharing.
        response.headers['Access-Control-Allow-Origin']='*'

        # Accepting data from a request
        reg_info = {"login"   : request.POST['login'], 
                    "email"   : request.POST['email'], 
                    "password": request.POST['password'], 
                    "DOB"     : request.POST['dob'], 
                    "location": request.POST['location']}

        # answer to be sent to the client
        answer = self.__validate_registration(reg_info)

        # adding a new user if no errors found
        if "SUCCESS" in answer.keys():
            new_user = User(reg_info["login"], 
                            reg_info["password"], 
                            reg_info["email"], 
                            reg_info["DOB"], 
                            reg_info["location"])
            Session.add(new_user)
            Session.commit()

        return answer
            
