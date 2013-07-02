import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from guessword.lib.base import BaseController, render

from pylons.decorators import jsonify
from guessword.model.meta import Session
from guessword.model.user import User
from guessword.model.training import Training
from sqlalchemy import func

log = logging.getLogger(__name__)

class TrainingController(BaseController):
    def __ratio(self, correct, incorrect):
        '''
        '''
        if correct + incorrect == 0:
            return 0
        else:
            return round(float(correct/(correct + incorrect)), 2)

    @jsonify
    def index(self):
        '''
        '''
        # Setting a response header to enable access control
        # using cross-origin resource sharing.
        response.headers['Access-Control-Allow-Origin']='*'

        # Accepting data from a request
        training_info = {"login"         : request.POST['login'], 
                         "trainings"     : int(request.POST['trainings']), 
                         "wordsCorrect"  : int(request.POST['wordsCorrect']), 
                         "wordsIncorrect": int(request.POST['wordsIncorrect']), 
                         "trainingTime"  : int(request.POST['trainingTime']), 
                         "totalScore"    : int(request.POST['totalScore']),
                         "trainDate"     : request.POST['trainDate']}
    
        query = Session.query(User).filter(User.Login == training_info["login"])
        id = query.first().UserID

        user_info = query.first()

        new_training = Training(id, 
                                training_info["trainings"], 
                                training_info["wordsCorrect"], 
                                training_info["wordsIncorrect"],
                                training_info["trainingTime"],
                                training_info["totalScore"],
                                self.__ratio(training_info["wordsCorrect"], training_info["wordsIncorrect"]),
                                training_info["trainDate"])
        Session.add(new_training)
        Session.commit()

        training_query = Session.query(func.count(Training.Trainings).label('training'),
                                        func.sum(Training.WordsCorrect).label('wordsCorrect'),
                                        func.sum(Training.WordsIncorrect).label('wordsIncorrect'),
                                        func.sum(Training.TrainingTime).label('trainingTime'),
                                        func.sum(Training.TotalScore).label('totalScore'),
                                        func.avg(Training.Ratio).label('ratioQuery')).\
                                        filter(Training.UserID == id).first()

        json_user = { 
            "training": {
                "app_trainings"     : training_query.training,
                "app_wordsCorrect"  : training_query.wordsCorrect,
                "app_wordsIncorrect": training_query.wordsIncorrect,
                "app_trainingTime"  : training_query.trainingTime, 
                "app_totalScore"    : training_query.totalScore,
                "app_ratio"         : training_query.ratioQuery
            }
        }
        return json_user
