from storage_interface import Store


class Default(Store):

    """
    TODO: Implement the storage inferface for Django. See the API
    specification in storage_interface.py for details about how to
    implement the stubs below.
    """

    def __init__(self):
        pass

    def get_submission(self):
        pass

    def set_compile_status(self, status, err_msg=None, submission_id=None):
        pass

    def get_test_group(self, problem_id=None):
        pass

    def set_test_group_score(self, score, problem_id=None,
                             test_group_id=None, submission_id=None):
        pass

    def set_submission_run_status(self, status, submission_id=None):
        pass

    def set_submission_score(self, score, submission_id=None):
        pass
