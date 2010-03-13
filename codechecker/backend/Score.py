# This class does the scoring for a submission using the results of
# all tests passed by it.

from codechecker.contests.models import Submission, Problem, TestCase, TestSet, Contest

class Score:
    
    def __init__(self, config):
        self.config = config

    def score(self, submission):

        if submission.result == "ACC":
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

