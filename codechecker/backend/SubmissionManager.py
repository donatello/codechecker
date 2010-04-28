# This class has methods to do all submission processing and
# evaluation tasks.

from Compile import *
from TestsRunner import TestsRunner
from Score import Score
from codechecker.Logger import Logger
from codechecker.contests.models import Submission, Problem, Testcase, TestSet, TestcaseEval

class SubmissionManager:
    
    def __init__(self, config):
        self.config = config
        self.compile = None
        self.log = Logger(__file__, config.config.get("BackendMain", "LogFile")).log

    def process_submission(self, submission):
        self.log('process_submission #%s' % str(submission.pk), Logger.DEBUG)

        # Compile the submission
        submission.result = "CMP"
        submission.save()
        res, err = self.do_compile(submission)
        
        if not res:
            submission.points = 0
            submission.penalty = 20
            submission.errors = err
            submission.result = "CMPE"
            submission.save()
            return

        # Run all testcases against the submission.
        self.do_test_and_evaluate(submission)

        # Score the submission
        if submission.result == "RUN":
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

        elif submission.language == 'java':  
            self.compile = Java_Compile(self.config)
            res, err = self.compile.compile(submission)
        
        else:
            pass
        
        return res, err
            
    def do_test_and_evaluate(self, submission):
        tests_runner = TestsRunner(self.config, self.compile, submission)
        tests_runner.run_tests()         
        
    def do_score(self, submission):
        prob = submission.problem
        testsets = TestSet.objects.filter(problem = prob)
        score_total = 0.0
        if prob.cust_eval != "":
            print "APPROX PROBLEM"
            scRange = prob.cust_maxScore - prob.cust_minScore
            for testset in testsets:
                testEvals = TestcaseEval.objects.filter(testcase__testSet = testset
                                                        ).filter(submission = submission)
                fails = testEvals.filter(pass_status = "FAILED")
                if len(fails) != 0:
                    submission.result = "WA"
                    score_total = 0
                    break
                else:
                    tscore = self.get_normalized_testset_score(prob, testset)
                score_total += tscore            
        else:
            print "NON-APPROX PROBLEM"
            for testset in testsets:
                testEvals = TestcaseEval.objects.filter(testcase__testSet = testset
                                                        ).filter(submission = submission)
                fails = testEvals.filter(pass_status = "FAILED")
                if len(fails) != 0:
                    submission.result = "WA"
                    score_total = 0
                    break
                else:
                    tscore = testset.maxScore
                score_total += tscore

        if submission.result == "RUN":
            submission.result = "ACC"

        submission.score = int(score_total) #truncating.
        submission.save()
                
    def get_normalized_testset_score(self, prob, testset):
        testEvals = TestcaseEval.objects.filter(testcase__testset_id = testset.pk)
        score_sum = testEvals.aggregate(avg = Avg('score'))["avg"]
        normalized_testset_score = (score_sum - prob.cust_minScore
                                    ) * testset.maxScore / (scRange*1.0) 
        return normalized_testset_score
    
