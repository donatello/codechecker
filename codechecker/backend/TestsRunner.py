# This class has methods to run each test against the submission and
# evaluate correctness.

class TestsRunner:
    
    def __init__(self, config):
        self.config = config

    # Main function for this class. Finds all testcases for this
    # submission and calls test() and evaluate() on each of them.
    def run_tests(self, submission):
        self.submission = submission

        all_testcases = None # Get all testcases from the db
        for testcase in all_testcases:
            test_result = self.test(testcase)
            self.evaluate(testcase, test_result)
            
        return

    # Runs the submission against a testcase.
    def test(self, testcase):
        pass

    # Evaluates the result of a run against a testcase.
    def evaluate(self, testcase, test_result):
        pass
