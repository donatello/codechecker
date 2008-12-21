#!/usr/bin/python
import sys
import time
import os
import threading

import Globals
import DbConnect



db = DbConnect.DbHandler()


def main():
    while Globals.CHECKER_STATUS :
        field = db.fetch()
        
        # default idle time out for the main loop is set as 2 seconds! 
        if(len(field) == 0 ) :
            time.sleep(2)
            log("No submission to handle")
            continue
        
        submission = Submission(field[0], field[2], field[3], field[4])
        Globalslog("Starting evaluation of Submission #%d for user %d for the problem %d" % submission.id,submission.uid,submission.pid)
        submission = HandleSubmission(submission)
        log("Finishing evaluation of Submission #%d for user %d for the problem %d" % submission.id,submission.uid,submission.pid)
        
        
        Globals.CHECKER_STATUS = False
    
# the main function call
if __name__ == "__main__":
    main()