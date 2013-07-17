# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging
import cgi

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from guessword.lib.base import BaseController, render
from pylons.decorators import jsonify

from guessword.model.meta import Session
from guessword.model.user import User
from guessword.model.trywords import Trywords
from guessword.model.training import Training
from sqlalchemy import func

log = logging.getLogger(__name__)

class WordController(BaseController):
    """Operates data used for training"""
    def setup(self):
        """
        Adds words to the dictionary.
        """
        words = {
            "to foster": ("заморожувати", "процвітати", "сприяти", "покращувати"),
            "invoice": ("накладна", "голос", "баланс", "шепіт"),
            "to prevail": ("попереджувати", "переважати", "передбачати", "підготувати"),
            "grief": ("горе", "відраза", "камінь", "дах"),
            "to transmit": ("лагодити", "перекладати", "розбивати", "передавати"),
            "vengeance": ("вегетеріанець", "прохання", "помста", "жорстокість"),
            "coward": ("приятель", "боягуз", "ковдра", "військовий"),
            "to acquire": ("вимагати", "сперичатись", "здобувати", "сумніватись"),
            "frequency": ("частота", "дивина", "залежність", "спокій"),
            "doubt": ("впеаненість", "впертість", "ворожість", "сумнів"),
        }

        for word in words:
            new_word = Trywords(word, words[word][0], words[word][1], words[word][2], words[word][3])
            Session.add(new_word)
            Session.commit()

    @jsonify
    def index(self):
        """
        Yavorovksy!
        """
        # Setting a response header to enable access control
        # using cross-origin resource sharing.
        response.headers['Access-Control-Allow-Origin']='*'      
        return  {"difficulty": "hard", "something":"else"}

    @jsonify
    def trywords(self):
        """
        Gets data from the trywords table and generates a JSON object
        containing words and possible translation varianls, having 
        a correct answer marked with 1, and incorrect with 0.
        """
        # Setting a response header to enable access control
        # using cross-origin resource sharing
        response.headers['Access-Control-Allow-Origin']='*'
        # the reply to be generated
        result = {}

        # addind words from BD 
        words_query = Session.query(Trywords)
        for word in words_query:
            key, value = Trywords.repr(word)
            result[key] = value

        return result
