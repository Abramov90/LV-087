# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging
from datetime import date

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from pylons.decorators import jsonify
from guessword.model.meta import Session
from guessword.model.user import User
from guessword.model.training import Training
from sqlalchemy import func

from guessword.lib.base import BaseController, render

log = logging.getLogger(__name__)

class LoginController(BaseController):

    def __user_exists(self, log_info):
        """Returns a user object and its training results if user with 
        specified login and password exists.

        :Parameters:
            log_info: (dict of str: unicode) Information entered by tne user.
        :Return:
            (class, class) User object if user exists anf None otherwise.
        """
        # checking if user with specified login and password exists
        query = Session.query(User).\
        filter(((User.Login == log_info["login"]) | (User.Email == log_info["login"])) \
            & (User.Password == log_info["password"]))
        
        if query.first():
            id = query.first().UserID
            # calculatimg the average results of a user
            training_query = Session.query(func.count(Training.Trainings).label('training'),
                                        func.sum(Training.WordsCorrect).label('wordsCorrect'),
                                        func.sum(Training.WordsIncorrect).label('wordsIncorrect'),
                                        func.sum(Training.TrainingTime).label('trainingTime'),
                                        func.sum(Training.TotalScore).label('totalScore'),
                                        func.avg(Training.Ratio).label('ratioQuery')).\
                                        filter(Training.UserID == id)

            return query.first(), training_query.first()

    def __calculate_user_age(self, user_info):
        """Returns age of the user.

        :Parameters:
            user_info: (class) User object.
        :Return:
            (int) Age of the user.
        """
        if user_info.DOB is not None:
            difference = date.today() - user_info.DOB
            age = difference.days//365
            return int(age)

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
        
        # responce
        json_user = {}

        # creating a JSON object with user info if such user exists
        try:
            user_info, training_info = self.__user_exists(log_info)
            json_user = { 
                "main": {
                    "login"   : user_info.Login, 
                    "email"   : user_info.Email,
                    "url"     : user_info.URL,
                    "age"     : self.__calculate_user_age(user_info),
                    "location": user_info.Location
                }, 
                "training": {
                    "app_trainings"     : training_info.training,
                    "app_wordsCorrect"  : training_info.wordsCorrect,
                    "app_wordsIncorrect": training_info.wordsIncorrect,
                    "app_trainingTime"  : training_info.trainingTime, 
                    "app_totalScore"    : training_info.totalScore,
                    "app_ratio"         : training_info.ratioQuery
                }
            }
        except TypeError:
            return json_user

        return json_user