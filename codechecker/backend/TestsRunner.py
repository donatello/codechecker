# This class has methods to run each test against the submission and
# evaluate correctness.

from codechecker.contests.models import Submission, Problem, TestCase, TestSet, Contest

class TestsRunner:
    
    def __init__(self, config, compile):
        self.config = config
        self.compile = compile

    # Main function for this class. Finds all testcases for this
    # submission and calls test() and evaluate() on each of them.
    def run_tests(self, submission):
        self.submission = submission
        testsets = TestSet.object.filter(problem=submission.problem)
        for testset in testsets:
            all_testcases = TestCase.objects.filter(testset_id=testset.id)
            for testcase in all_testcases:
                test_result = self.test(testcase)
                self.evaluate(testcase, test_result)
            

    # Runs the submission against a testcase.
    def test(self, testcase):
        pass
 
    # Evaluates the result of a run against a testcase.
    def evaluate(self, testcase, test_result):
        pass
