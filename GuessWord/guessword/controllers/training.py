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
        """Returns a value of correct words divided by the number of total words.

        :Parameters:
            correct  : (int) The number of words answered correctly.
            incorrect: (int) The number of words answered incorrectly.
        :Return:
            (float) The number indicating the precentage of words answered correctly.
        """
        if correct + incorrect == 0:
            return 0
        else:
            return float(correct)/(correct + incorrect)

    def __find_user(self, email):
        """Returns ID of a user with a given email.

        :Parameters:
            email: (string) The user's email.
        :Return:
            (rowTuple) The ID of the user with a given email.
        """
        query = Session.query(User).filter(User.Email == email)

        return query.first().UserID

    def __generate_training_results(self, id):
        """Returns training info of a user with given id.

        :Parameters:
            id: (rowTuple) The user's id.
        :Return:
            (object) Training info of a user from the training DB table.
        """
        # calculating general info about all of the user's trainings
        training_query = Session.query(func.count(Training.UserID).label('training'),
                                        func.sum(Training.WordsCorrect).label('wordsCorrect'),
                                        func.sum(Training.WordsIncorrect).label('wordsIncorrect'),
                                        func.sum(Training.TrainingTime).label('trainingTime'),
                                        func.sum(Training.TotalScore).label('totalScore'),
                                        func.avg(Training.Ratio).label('ratioQuery')).\
                                        filter(Training.UserID == id).first()
        # adding the calculated above info to JSON
        json_user = { 
            "trainings"     : training_query.training,
            "wordsCorrect"  : training_query.wordsCorrect,
            "wordsIncorrect": training_query.wordsIncorrect,
            "trainingTime"  : training_query.trainingTime, 
            "totalScore"    : training_query.totalScore,
            "ratio"         : training_query.ratioQuery
        }
        return json_user

    @jsonify
    def post(self):
        """Accepts data about the new training and adds it to DB.
        Returns a JSON representation of user training data, 
        according to the email sent by the client.
        """
        # Setting a response header to enable access control
        # using cross-origin resource sharing.
        response.headers['Access-Control-Allow-Origin']='*'

        # Accepting data from a request
        email = request.POST['email']
        wordsCorrect = int(request.POST['wordsCorrect'])
        wordsIncorrect = int(request.POST['wordsIncorrect'])
        trainingTime = int(request.POST['trainingTime'])
        totalScore = int(request.POST['totalScore'])
        trainDate = request.POST['trainDate']

        # finding id of a user according to the email sent in request
        id = self.__find_user(email)

        # generating a new training object and adding it to database
        new_training = Training(id, wordsCorrect, wordsIncorrect, trainingTime, \
            totalScore, self.__ratio(wordsCorrect, wordsIncorrect), trainDate)
        Session.add(new_training)
        Session.commit()

        # calculatimg the average results of a user and creating a JSON object
        json_user = self.__generate_training_results(id)
        return json_user

    @jsonify
    def get(self):
        """Returns a JSON representation of user training data, 
        according to the email sent by the client.
        """
        # Setting a response header to enable access control
        # using cross-origin resource sharing.
        response.headers['Access-Control-Allow-Origin']='*'

        # Accepting data from a request
        email = request.POST['email']

        # finding id of a user according to the email sent in request
        id = self.__find_user(email)

        # calculatimg the average results of a user and creating a JSON object
        json_user = self.__generate_training_results(id)
        return json_user