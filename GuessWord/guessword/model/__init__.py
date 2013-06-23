"""The application's model objects"""
from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, String, Date, Unicode
from sqlalchemy import Unicode
from guessword.model.meta import Session, Base

def init_model(engine):
    """Call me before using any of the tables or classes in the model"""
    Session.configure(bind=engine)

    global User
    class User(Base):
        '''Establishes the connection with a user table in DB.
        '''
        __tablename__ = 'user'
        
        ID       = Column(Integer, primary_key=True)
        Login    = Column(Unicode)
        Password = Column(Unicode)
        Email    = Column(String)
        DOB      = Column(Date)
        Location = Column(Unicode)

        def __init__(self, login, password, email, DOB, location):
            self.Login    = login
            self.Password = password
            self.Email    = email
            self.DOB      = DOB
            self.Location = location
