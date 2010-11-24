from checker.cc_frontend.web.models import Contest
from checker.cc_frontend.web.models import Problem
from checker.cc_frontend.web.models import Submission
from checker.cc_frontend.web.models import TestSet
from checker.cc_frontend.web.models import Testcase
import os
from storage_interface import Store


class Default(Store):

    """
    TODO: Implement the storage inferface for Django. See the API
    specification in storage_interface.py for details about how to
    implement the stubs below.
    """

    def __init__(self, config):
        self.config = config

    def get_submission(self):
        try 
            q_sub = Submission.objects.filter(result='QU')[0]
            src_fname = os.path.join(self.config.abs_path, str(q_sub.pk) +
                        '.' + q_sub.language)
            src_file = open(src_fname, 'w')
            src_file.write(q_sub.code)
            src_file.close()

            ret['src_file'] = src_fname 
            ret['prob_id'] = str(q_sub.problem)
            ret['id'] = str(q_sub.pk)
            return ret

        except IndexError:
            print "No queued submission found"
            return None

    def set_compile_status(self, status, err_msg=None, submission_id=None):
        q_sub = Submission.objects.filter(pk=int(submission_id))
        q_sub.result = status
        q_sub.errors = err_msg
        q_sub.save()

    def get_test_group(self, problem_id=None):
        q_tgs = TestSet.objects.filter(problem=int(problem_id))
        for q_tg in q_tgs:
            ret_tg['prob_id'] = problem_id
            ret_tg['testgroup_id'] = str(q_tg.pk)
            ret_tg['timelimit'] = q_tg.timelimit
            ret_tg['memlimit'] = q_tg.memlimit
            ret_tg['score'] = q_tg.score 
            ret_tg['is_cust_scored'] = q_tg.is_cust_scored 
            ret_tg['cust_execute'] = q_tg.cust_executable 
            ifnames = [] 
            ofnames = []
            q_tcs = Testcase.objects.filter(testset=q_tg.pk)
            for q_tc in q_tcs:
                ifname = os.path.join(self.config.abs_path, str(q_tc.pk) +
                            '.in')
                in_file = open(ifname, 'w')
                in_file.write(q_tc.input)
                in_file.close()
                ifnames.append(ifname)
                ofname = os.path.join(self.config.abs_path, str(q_tc.pk) +
                            '.ref')
                on_file = open(ofname, 'w')
                on_file.write(q_tc.output)
                on_file.close()
                ofnames.append(ofname)

            ret_tg['input_files'] = ifnames
            ret_tg['output_files'] = ofnames
            yield ret_tg


    def set_test_group_score(self, score, problem_id=None,
                             test_group_id=None, submission_id=None):
        pass

    def set_submission_run_status(self, status, submission_id=None):
        q_sub = Submission.objects.filter(pk=int(submission_id))
        q_sub.result = status
        q_sub.save()

    def set_submission_score(self, score, submission_id=None):
        q_sub = Submission.objects.filter(pk=int(submission_id))
        q_sub.score = score
        q_sub.save()
