class Store:
    """
    This is the base class for the storage interface. The default
    interface will be interface with Django's models. This module can
    be derived and made to work any other kind of storage system too
    like NOSQL, etc.
    """

    def __init__(self):
        """
        Initialize any storage connections here.
        """
        pass

    def get_submission(self):
        """
        Fetches a submission from the store. If there is no queued
        submission, it returns None immediately. If a queued
        submission is found, it atomically sets the status of the
        submission to "processing"

        Returns a pair (problem_id, submission)

        submission is an object that contains the path to the source
        file and the submission id.
        """
        pass

    def set_compile_status(self, status, err_msg=None, submission_id=None):
        """
        Sets the compile status of submission to success/failure.
        """
        pass

    def get_test_group(self, problem_id=None):
        """
        A test_group is a dictionary containing a list of input files
        and corresponding ref_output objects. The output ref_output
        objects are either reference output files or a binary program
        that can check the output produced by the submission.

        The returned dictionary also contains an attribute that
        identifies the test_group id. This is used in the scoring
        module to identify the scoring algorithm to use.

        This function should be implemented as a python generator. The
        Evaluation module calls this function repeatedly to get each
        test_group successively.
        """
        pass

    def set_test_group_score(self, score, problem_id=None,
                             test_group_id=None, submission_id=None):
        """
        Sets the score for a submission for a test_group
        """
        pass

    def set_submission_run_status(self, status, submission_id=None):
        """
        After evaluation of test cases, this function sets the status
        of the program to "PASS", "FAIL" or some execution error
        status.
        """
        pass

    def set_submission_score(self, score, submission_id=None):
        """
        Sets the overall score for a submission.
        """
        pass
