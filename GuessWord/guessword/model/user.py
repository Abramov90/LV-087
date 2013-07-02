"""The application's user model"""
from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, String, Date, Unicode
from sqlalchemy import Unicode
from guessword.model.meta import Session, Base


global User
class User(Base):
    '''Establishes the connection with a user table in DB.
    '''
    __tablename__ = 'user'
    
    UserID     = Column(Integer, primary_key=True)
    Login      = Column(Unicode)
    Password   = Column(Unicode)
    Email      = Column(String)
    DOB        = Column(Date)
    Location   = Column(Unicode)
    URL        = Column(String)
    FacebookID = Column(Unicode)

    def __init__(self, login, password, email, DOB, location, facebookID="", url="http://guessword.com/"):
        self.Login      = login
        self.Password   = password
        self.Email      = email
        self.DOB        = DOB
        self.Location   = location
        self.URL        = url
        self.FacebookID = facebookID