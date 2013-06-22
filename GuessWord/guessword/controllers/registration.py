# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging

from pylons.decorators import jsonify
from guessword.model.meta import Session
from guessword.model import User
import re


from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from guessword.lib.base import BaseController, render

log = logging.getLogger(__name__)

class RegistrationController(BaseController):

    def __email_check(self, email):
        """Returns True if user with specified email already exists in DB.
        """
        email_exists = \
                Session.query(User.Email).filter(User.Email == email).count()
        if email_exists:
            return True

    def __login_check(self, login):
        """Returns True if user with specified login already exists in DB.
        """
        login_exists = \
                Session.query(User.Login).filter(User.Login == login).count()
        if login_exists:
            return True

    def __dob_check(self, DOB):
        """Returns True if user has entered DOB data in a wrong format.
        """
        if str(DOB) != '' and re.match("\d{4}-\d{2}-\d{2}", str(DOB)) == None:
            return True

    @jsonify
    def index(self):
        """Adds a new user to the user table if another user
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

        # objects needed to be checked
        validate =  {'login': self.__login_check,
                     'email': self.__email_check,
                     'DOB'  : self.__dob_check}

        # answer to be created                     
        answer = []

        # possible error messases
        message = ["app_login_error",
                   "app_email_error",
                   "app_date_format_YYYY-MM-DD_error",
                   "success"]

        # validation
        for num, field in enumerate(("login", "email", "DOB")):
            if validate[field](reg_info[field]):
                answer.append(message[num])

        if answer == []:
            new_user = User(reg_info["login"], 
                            reg_info["password"], 
                            reg_info["email"], 
                            reg_info["DOB"], 
                            reg_info["location"])
            Session.add(new_user)
            Session.commit()
            answer.append(message[-1])       
        return  {"ANSWER": answer}
            
