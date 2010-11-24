#!/usr/bin
import sys
import os
import string
import time
import threading

from store.default_store import Default
from evaluator.eval import Evaluate
from compiler.compile import Compiler
from score.score import Score
from Config import Config


def main():

    config = Config("conf/codechecker.conf")
    store = Default(config)
    evaluator = Evaluate(config)
    compiler = Compiler(config)
    score = Score()

    is_waiting = True

    while True:
        # get a queued submission.
        submission = store.get_submission()

        # if no submission is found wait for one.
        if submission is None:
            if not is_waiting:
                is_waiting = True
                print "Waiting for a submission."
            time.sleep(2)
            continue

        is_waiting = False

        # compile the submission
        compiler_res = compiler.compile_source(submission["src_file"])
        if compiler_res["retcode"] == 0:
            store.set_compile_status("COMPILED", err_msg=None,
                                     sub_id=submission["id"])
        else:
            store.set_compile_status("COMPILATION ERROR",
                                     err_msg=status_info.err_msg,
                                     sub_id=submission["id"])
            continue

        # Evaluate the queued submission. Somewhere in the following
        # loop it is also possible that the program fails - need to
        # set the status to runtime error status.
        test_group_scores = []
        for test_grp in store.get_test_group(submission["prob_id"]):
            result_set = evaluator.eval_submission(submission,
                                                   test_grp, compiler_res["run_cmd"])
            test_grp_score = score.score_group(prob_id,
                                               result_set)
            store.set_test_group_score(test_grp_score,
                problem_id=prob_id, test_group_id=test_grp["id"],
                submission_id=submission["id"])
            test_group_scores.append(test_grp_score)

        # compute and set the overall score.
        final_score = score.overall(test_group_scores,
                                    problem_id=prob_id)
        store.set_submission_score(final_score,
                                   submission_id=submission["id"])
        store.set_submission_run_status("PASS",
                                        submission_id=submission["id"])


if __name__ == '__main__':
    main()
