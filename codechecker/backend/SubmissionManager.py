# This class has methods to do all submission processing and
# evaluation tasks.

from Compile import Compile
from TestsRunner import TestsRunner
from Score import Score

class SubmissionManager:
    
    def __init__(self, config):
        self.config = config

    def process_submission(self, submission):
        
        self.do_compile(submission)

        self.do_test_and_evaluate(submission)

        self.do_score(submission)

        return

    def do_compile(self, submission):
        pass

    def do_test_and_evaluate(self, submission):
        pass

    def do_score(self, submission):
        pass
    
