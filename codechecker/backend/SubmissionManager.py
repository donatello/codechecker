# This class has methods to do all submission processing and
# evaluation tasks.

from Compile import *
from TestsRunner import TestsRunner
from Score import Score
from codechecker.Logger import Logger


class SubmissionManager:
    
    def __init__(self, config):
        self.config = config
        self.compile = None
        self.log = Logger(__file__, config.config.get("BackendMain", "LogFile")).log

    def process_submission(self, submission):
        self.log('process_submission #%s' % str(submission.pk), Logger.DEBUG)
        submission.result = "CMP"
        res, err = self.do_compile(submission)

        if not res:
            submission.points = 0
            submission.penalty = 20
            submission.errors = err
            submission.result = "CMPE"
            submission.save()
            return

        self.do_test_and_evaluate(submission)

        self.do_score(submission)

        return

    def do_compile(self, submission):
        if submission.language == 'c':
            self.compile = C_Compile(self.config)
            res, err = self.compile.compile(submission)

        elif submission.language == 'cpp':  
            self.compile = CPP_Compile(self.config)
            res, err = self.compile.compile(submission)

        elif submission.language == 'p':  
            self.compile = Pascal_Compile(self.config)
            res, err = self.compile.compile(submission)

        elif submission.language == 'py':  
            self.compile = Python_Compile(self.config)
            res, err = self.compile.compile(submission)
        
        else:
            pass
        
        return res, err
            
    def do_test_and_evaluate(self, submission):
        tests_runner = TestsRunner(self.config, self.compile, submission)
        tests_runner.run_tests()         
        



    def do_score(self, submission):
        pass
    
