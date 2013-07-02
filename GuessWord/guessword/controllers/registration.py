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
        """Returns True if user with specified email already exists in DB.

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
        """Returns True if user with specified login already exists in DB.

        :Parameters:
            login: (unicode) A login provided by the user.
        :Return:
            (bool) True if login exists in DB and False otherwise.
        """
        login_exists = \
                Session.query(User.Login).filter(User.Login == login).count()
        if login_exists:
            return True

    def __dob_check(self, DOB):
        """Returns True if user has entered DOB data in a wrong format.

        :Parameters:
            DOB: (unicode) A date of birth provided by user.
        :Return:
            (bool) True if DOB is of wrong format and False otherwise.
        """
        if str(DOB) != '' and re.match("\d{4}-\d{2}-\d{2}", str(DOB)) == None:
            return True

    def __validate_registration(self, reg_info):
        """Returns message ["success"] if user entered data in a required 
        format and unique login and email 
        Otherwise returns a list of errors.

        :Parameters:
            reg_info: (dict of str: unicode) Information about the user.
        :Return:
            (list of str) A list of errors found.
        """
        # objects needed to be checked
        validate =  {'login': self.__login_check,
                     'email': self.__email_check,
                     'DOB'  : self.__dob_check}

        # answer to be created                     
        answer = []

        # possible error messases
        message = ["app_login_error",
                   "app_email_error",
                   "app_date_format_YYYY-MM-DD_error"]

        # validation
        for num, field in enumerate(("login", "email", "DOB")):
            if validate[field](reg_info[field]):
                answer.append(message[num])

        # appending success message if no errors found
        if answer == []:
            answer.append("success")

        return answer

    def __send_email(self, user_password, reg_info):
        "Sends an email to the user with his login and password."
        import smtplib
        import datetime

        from_addr = 'guessword@gmail.com'  
        to_addr  = reg_info["email"] 

        subj = "GuessWord registration"
        date = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")

        message_text = "Wellcome to GuessWord!\nYour login: %s\nYour password:%s\n\nThank you!\n" \
        % (reg_info["login"], user_password)

        msg = "From: %s\nTo: %s\nSubject: %s\nDate: %s\n\n%s" \
        % (from_addr, to_addr, subj, date, message_text)

        username = 'iryna.rushchyshyn'  
        password = 'cheesecl0th'  

        server = smtplib.SMTP('smtp.gmail.com:587')  
        server.starttls()  
        server.login(username, password)  
        server.sendmail(from_addr, to_addr, msg)  
        server.quit()

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

        # answer to be sent to the client
        answer = self.__validate_registration(reg_info)

        # adding a new user if no errors found
        if answer == ["success"]:
            self.__send_email(reg_info["password"], reg_info)
            new_user = User(reg_info["login"], 
                            reg_info["password"], 
                            reg_info["email"], 
                            reg_info["DOB"], 
                            reg_info["location"])
            Session.add(new_user)
            Session.commit()

        return  {"ANSWER": answer}
            
