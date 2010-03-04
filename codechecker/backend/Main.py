#!/usr/bin
import sys
import os
import string
import time
import threading

sys.path.append("/opt/checker")
from codechecker.contests.models import Submission,Problem
#from utils.Logger import Logger as log
from Handler import *
from Config import Config


def main():

    config = Config()
    submissionHandler = SubmissionHandler(config)
    
    while 1:
        #submissions is a list of model-instance objects (not dictionary)
        submissions = Submission.objects.filter(result='QU')[:1]
        
        if len(submissions) == 0 :
            time.sleep(2)
            log('No Submission to handle')
            continue
        submission = submissions[0]
        log('Starting evaluation of Submission #%s' % str(submission.pk))
        submissionHandler.handle_submission(submission)    
        log('Finishing processing Submission #%s\n' % str(submission.pk))
    
    
if __name__ == '__main__':
    main()
