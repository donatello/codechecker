#!/usr/bin
import sys
import os
import string
import time
import threading

from contests.models import Submission,Problem
from backend.Handler import *

os.putenv('DJANGO_SETTINGS_MODULE','settings')


def main():
    
    while 1:
        submissions = Submission.objects.filter(result='QU')[:1].values('ID', 'lang','code', 'user', 'comments', 'result', 'problem')
        
        if len(submissions) == 0 :
            time.sleep(2)
            log('No Submission to handle')
            continue
        submission = submissions[0]
        log( 'Starting evaluation of  Submission #%s\n' % str(submission['ID']))
        handle_submission(submission)    
        log( 'Finishing processing Submission #%s\n' % str(submission['ID']))
        time.sleep(2)
    
    
if __name__ == '__main__':
    main()
