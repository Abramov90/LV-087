from guessword.tests import *

class TestTrainingController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='training', action='index'))
        # Test response...
