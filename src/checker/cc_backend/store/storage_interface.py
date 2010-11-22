class Store:
    """
    This is the base class for the storage interface. The default
    interface will be interface with Django's models. This module can
    be derived and made to work any other kind of storage system too
    like NOSQL, etc.

    The requirements for the objects passed and returned by each
    function are found in the function's comments below.

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
        submission to "processing" in the persistent storage.

        Arguments: None

        Returns: None if no submission is queued at the
        moment. Otherwise a dictionary with the following key/value
        pairs:

        {
            "src_file" : "/path/to/source_file",
            "prob_id"  : "a string representing the id",
            "id"   : "string, id of submission"
        }

        """
        pass

    def set_compile_status(self, status, err_msg=None, sub_id=None):
        """
        Sets the compile status of submission to success/failure.

        Arguments: status -> a string representing the status:
                   is either "SUCCESS" or "FAILURE"
                   err_msg -> a string representing the compiler
                   error message, if any; None otherwise
                   sub_id -> the string id of the submission

        Returns: None
        """
        pass

    def get_test_group(self, prob_id=None):
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

        Arguments: prob_id -> string id of the problem.

        Returns: A testgroup object in each successive call until no
        more remains. A testgroup object is a dictionary with the
        following key/value pairs:

        {
             "prob_id" : "string problem id",

             "testgroup_id" : "string id for testgroup",

             "timelimit" : "time limit for a submisson for this testgroup",

             "memlimit" : "memory limit for a submisson for this testgroup",

             "input_files" : [list of input file names] each of the form 
                                submission_id.in and corresponding outfile
                                and errfile would be submission_id.{out, err},

             "output_files" : [list of corresponding reference output
                              file names] or None if a separate
                              program evaluates the outputs produced,

             "cust_execute" : binary to execute as checker program
                              (TODO write details of semantics),

             "score" : The int score if all cases in this testgroup
                       pass,

             "is_cust_scored" : A flag, if True indicates that
                                cust_execute produces the score for
                                each input file (total score for group
                                is the sum)
        }

        """
        pass

    def set_testgroup_score(self, score, testgroup_id=None,
                            sub_id=None):
        """
        Sets the score for a submission for a testgroup
        """
        pass

    def set_submission_run_status(self, status, sub_id=None):
        """
        After evaluation of test cases, this function sets the status
        of the program to "ACCEPTED", "WRONG ANSWER" or some execution
        error status.
        """
        pass

    def set_submission_score(self, score, sub_id=None):
        """
        Sets the overall score for a submission.
        """
        pass
