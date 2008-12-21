#!/usr/bin/python

import os
from DbConnect import *



# Checker Global variables
CHECKER_STATUS = True
MAX_HANG_WAIT = 180
RUNS_PATH = '/share/checker/runs/'
PROBLEM_PATH = '/share/checker/probs/'
SUBMISSION_PATH = '/share/checker/submissions/'

OUTPUT_FILE_SIZE = int(128 << 20)    #max 128 MB
USER_ID = os.getuid()
GROUP_ID = os.getgid()

#ERRORS and RESULTS

QUEUED = -1
COMPILE_ERROR = 1
RUN_ABORT = 2
TIME_LIMIT_EXCEEDED = 3
MEMORY_LIMIT_EXCEEDED = 4
WRONG_ANSWER = 5
PRESENTATION_ERROR = 6
OUTPUT_ERROR = 7
FORK_ERROR = 8
FLOATING_POINT_EXCEPTION = 9
SEGMENTATION_FAULT = 10

PRESENTATION_ERROR = 11
ACCEPTED = 0


from DbConnect import *

def log( msg ):
    #logfile = file.open('log.txt','a')
    print msg

def check_files(outfile, chkfile):
    diff_out = os.popen('diff  '+ chkfile + ' ' + outfile)
    if len(diff_out) == 0:
        return ACCEPTED
    
    diff_out = os.popen('diff --ignore-blank-lines '+ chkfile + ' ' + outfile)
    if len(diff_out) == 0:
        return PRESENTATION_ERROR
    
    return WRONG_ANSWER
        

class Submission():
    def __init__(self,id,pid,uid,lang):
        db = dbHandler()
        self.id = id
        self.lang = lang
        self.pid = pid
        self.uid = uid
        file_name = SUBMISSION_PATH + db.getUserName(uid) +'/' + db.getProblemName(pid) 
        
        if ( lang == 'C') :
            file_name = file_name + '.c'

        elif ( lang == 'C++') :
            file_name = file_name + '.cc'

        elif ( lang == 'JAVA') :
            file_name = file_name + '.java'
            
        self.file = file_name
        self.result = QUEUED
        self.compile_error = ''
        self.run_error = ''
        