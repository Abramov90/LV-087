from guessword.tests import *

class TestWordController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='word', action='index'))
        # Test response...
