#!/usr/bin
import sys
import os
import string
import time
import threading

from store.default_storage import Default
from evaluator.eval import Evaluate
from compiler.compile import Compiler
from score.score import Score


def main():

    store = Default()
    evaluator = Evaluate()
    compiler = Compiler()
    score = Score()

    is_waiting = True

    while True:
        # get a queued submission.
        prob_id, submission = store.get_submission()

        # if no submission is found wait for one.
        if submission is None:
            if not is_waiting:
                is_waiting = True
                print "Waiting for a submission."
            time.sleep(2)
            continue

        is_waiting = False

        # compile the submission
        status_info, program = compiler.compile(submission)
        if status_info.status = "OK":
            store.set_compile_status("COMPILED", err_msg=None,
                                     submission["id"])
        else:
            store.set_compile_status("COMPILATION ERROR",
                                     err_msg=status_info.err_msg,
                                     submission["id"])
            continue

        # Evaluate the queued submission. Somewhere in the following
        # loop it is also possible that the program fails - need to
        # set the status to runtime error status.
        test_group_scores = []
        for test_grp in store.get_test_group(prob_id):
            result_set = evaluator.eval_submission(submission,
                                                   test_grp)
            test_grp_score = score.score_group(prob_id,
                                               result_set)
            store.set_test_group_score(test_grp_score,
                problem_id=prob_id, test_group_id=test_grp["id"],
                submission_id=submission["id"])
            test_group_scores.append(test_grp_score)

        # compute and set the overall score.
        final_score = score.overall(test_grp_scores,
                                    problem_id=prob_id)
        store.set_submission_score(final_score,
                                   submission_id=submission["id"])
        store.set_submission_run_status("PASS",
                                        submission_id=submission["id"])


if __name__ == '__main__':
    main()
