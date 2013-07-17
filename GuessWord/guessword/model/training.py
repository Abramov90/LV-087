"""The application's training model"""
from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, String, Date, Unicode, Float
from sqlalchemy import ForeignKey
from sqlalchemy import Unicode
from guessword.model.meta import Session, Base
from guessword.model.user import User


global Training
class Training(Base):
    """Establishes the connection with a training table in DB."""
    __tablename__ = 'training'
    
    TrainID        = Column(Integer, primary_key=True)
    UserID         = Column(Integer, ForeignKey('user.UserID'))
    WordsCorrect   = Column(Integer)
    WordsIncorrect = Column(Integer)
    TrainingTime   = Column(Integer)
    TotalScore     = Column(Integer)
    Ratio          = Column(Float)
    TrainDate      = Column(Date)

    def __init__(self, userID, wordsCorrect=0, wordsIncorrect=0, trainingTime=0, totalScore=0, ratio=0, trainDate="0000-00-00"):
        self.UserID         = userID
        self.WordsCorrect   = wordsCorrect
        self.WordsIncorrect = wordsIncorrect
        self.TrainingTime   = trainingTime
        self.TotalScore     = totalScore
        self.Ratio          = ratio
        self.TrainDate      = trainDate

    def create_JSON_training(self):
        """Returns a JSON representation of training results"""
        return {"trainings": self.UserID, "wordsCorrect": self.WordsCorrect , \
        "wordsIncorrect": self.WordsIncorrect, "trainingTime": self.TrainingTime, \
        "totalScore": self.TotalScore, "ratio": self.Ratio}