# This class has methods to do all submission processing and
# evaluation tasks.

from Compile import *
from TestsRunner import TestsRunner
from Score import Score

class SubmissionManager:
    
    def __init__(self, config):
        self.config = config
        self.compile = None

    def process_submission(self, submission):
        
        submission.result = "CMP"
        res, err = self.do_compile(submission)

        if not res:
            submission.submissionPoints = 0
            submission.submissionPenalty = 20
            submission.result = "CMPE"
            submission.save()

        self.do_test_and_evaluate(submission)

        self.do_score(submission)

        return

    def do_compile(self, submission):
        if submission.submissionLang == 'C':
            self.compile = C_Compile(self.config)
            res, err = c_compile.compile(submission)

        elif submission.submissionLang == 'CPP':  
            self.compile = CPP_Compile(self.config)
            res, err = cpp_compile.compile(submission)
        
        else:
            pass
        
        return res, err
            
    def do_test_and_evaluate(self, submission):
        tests_runner = TestsRunner(self.config, self.compile)
        tests_runner.run_tests(submission)         
        



    def do_score(self, submission):
        pass
    
