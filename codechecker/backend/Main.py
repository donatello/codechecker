#!/usr/bin
import sys
import os
import string
import time
import threading

sys.path.append("/opt/checker")
from codechecker.contests.models import Submission,Problem
from codechecker.Logger import Logger
from Config import Config
from SubmissionManager import SubmissionManager


def main():

    config = Config()
    sub_manage = SubmissionManager(config)
    log = Logger(__file__, config.config.get("BackendMain", "LogFile")).log
    
    while 1:
        try:
            # get a queued submission from the db.
            submission = Submission.objects.filter(result='QU')[0]
            log('Starting evaluation of Submission #%s' % str(submission.pk), Logger.DEBUG)
            sub_manage.process_submission(submission)
            log('Finished processing Submission #%s' % str(submission.pk), Logger.DEBUG)
        
        except IndexError:
            time.sleep(2)
            log('No Submission to handle', Logger.DEBUG)
    
    
if __name__ == '__main__':
    main()
