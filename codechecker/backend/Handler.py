import os
import sys
import time
import string

from codechecker.contests.models import Submission,Problem,TestCase,Contest
from SimpleChecker import SimpleChecker
from codechecker.Logger import log

class SubmissionHandler:
    config = None
    
    def __init__(self, config):
        self.config = config

    def handle_simple_checker(self, submission):
        tests = TestCase.objects.filter(problem=submission.problem)

        # set submission status to running
        submission.result = "RUN"
        submission.save()

        # Initialize SimpleChecker
        simplechecker = SimpleChecker(self.config)

        for test in tests:
            print str(test.pk)       
            simplechecker.run(submission, test)
            #reload the submission data from the db
            submission = Submission.objects.get(id = submission.id)
            if submission.result != 'RUN':
                break

        if submission.result == "RUN":
            submission.result = "ACC"

            # set points for the submission
            submission.submissionPoints = Problem.objects.get(id = submission.problem_id
                                                              ).maxScore        
            # set the penalty for the submission
            contestid = Problem.objects.get(id = submission.problem_id).contest_id
            contest = Contest.objects.get(id = contestid)
            tdelta = submission.submissionTime - contest.startDateTime
            minutes = tdelta.days*24*60 + tdelta.seconds/60
            submission.submissionPenalty = minutes
        else:
            #set the points and penalty for the submission
            submission.submissionPoints = 0
            submission.submissionPenalty = 20

        submission.save()

    # The 'submission' argument is a model-instance (not a dictionary).
    def handle_submission(self, submission):

        #write the submission code to a file.
        submission.write_code_to_disk(self.config.runpath)

        # compile the submission
        compiler_out = submission.compile(self.config.runpath)

        # check the compile result.
        if not(submission.check_compile_result(self.config.runpath)):
            log(compiler_out)
            log("Compilation failure #%s\n" % str(submission.pk))
            #set the points and penalty for the submission
            submission.submissionPoints = 0
            submission.submissionPenalty = 20
            submission.save()
            return

        # Compilation is successful. So proceeding.

        compiler_out += "Compilation Successful\n"
        log("Compilation Successful for submission #%s" % str(submission.pk))

        # Evaluate the submission's generated executable.
        self.handle_simple_checker(submission)
