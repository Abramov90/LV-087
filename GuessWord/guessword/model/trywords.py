# -*- coding: utf-8 -*-
"""The applications trywords model"""
from __future__ import unicode_literals
from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, String, Date, Unicode
from sqlalchemy import Unicode
from guessword.model.meta import Session, Base


global Trywords
class Trywords(Base):
    """Establishes the connection with a table in DB"""
    __tablename__ = 'trywords'
    
    WordID     = Column(Integer, primary_key=True)
    Word       = Column(Unicode)
    Translation= Column(Unicode)
    Incorrect1 = Column(Unicode)
    Incorrect2 = Column(Unicode)
    Incorrect3 = Column(Unicode)

    def __init__(self, word, translation, incorrect1, incorrect2, incorrect3):
        self.Word        = word
        self.Translation = translation
        self.Incorrect1  = incorrect1
        self.Incorrect2  = incorrect2
        self.Incorrect3  = incorrect3

    def repr(self):
        variants = {self.Translation: "1", self.Incorrect1: "0", self.Incorrect2: "0", self.Incorrect3: "0"}
        return self.Word, variants

