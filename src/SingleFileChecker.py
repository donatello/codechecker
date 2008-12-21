#!/usr/bin/python
import os
import sys
import resource
import string
import datetime
import time
import signal

from Globals import *
from DbConnect import *

def execute(submission):
    pass

def run(submission):

    dbase = DbHandler()
    pid = submission.pid
    pcode = dbase.getProblemName(pid)
    tlimit = dbase.getTimeLimit(pid)
    mlimit = (dbase.getMemLimit(pid))<<20
    executable = RUNS_PATH + str(pid) 
    infile = PROBLEM_PATH + pcode + '.in' 
    outfile = RUNS_PATH + str(pid) + '.out'
    errorfile = RUNS_PATH + str(pid) + '.err'
    chkfile = PROBLEM_PATH + pcode + '.out'
    
    log("Running %s with input file as %s and output file as %s" % executable,infile,outfile)
    
    run_messages = str()
    
    childId = os.fork()
    if childId == -1 :
        submission.result = FORK_ERROR
        return submission
    
    # within child thread
    if childId == 0:
        # set the input ,ouput and error streams
        sys.stdin = open(infile,'r')
        sys.stderr = open(errorfile,'w')
        sys.stdout = open(outfile,'w')
        
        # for when the child could not be killed just like that ! 
        os.seteuid(USER_ID + 11)
        os.setgid(GROUP_ID + 11)
        
        #resource limits are typically a tuple of (soft,hard) values as used.        
        
        #set the time limit for the process
        resource.setrlimit(RLIMIT_CPU,(tlimit,tlimit+1))
        
        #set the output file date size
        resource.setrlimit(RLIMIT_FSIZE,(OUTPUT_FILE_SIZE,OUTPUT_FILE_SIZE))
        
        #set the stack,heap limits
        resource.setrlimit(RLIMIT_STACK,(mlimit,mlimit))
        resource.setrlimit(RLIMIT_DATA,(mlimit,mlimit))
        resource.setrlimit(RLIMIT_DATA,(mlimit,mlimit))
        
        #disable forking
        #the 2 process limit get used up any way !
        resource.setrlimit(RLIMIT_NPROC,(2,2))
        
        #execute the test case
        ret = execute(submission)
        
        #exit from the child thread
        sys.exit(ret)
        
    # in the parent thread
    if childId :
        start_time = time.time()
        while time.time() < (start_time + MAX_HANG_WAIT) :
            pid,stat = os.waitpid(childId, os.WNOHANG)
            if pid == 0 :
                break
            sleep(0.01)
        
        pid,stat = os.waitpid(childId, os.WNOHANG)
        
        # if the process has still not exit, have to kill them manually
        if pid != 0 :
            
            log('The process has not been killed yet, killing manually')
            temp = os.kill(childId, 9)
        
            # if the process is still not getting killed 
            if temp == 0 :
                # create a fork and then fork,
                killChild = os.fork()
                if killChild == 0:
                    # set the fork userid same as the hung process
                    os.setuid(USER_ID+11)
                    os.setgid(GROUP_ID+11)
                    
                    # kill all processes that could be killed by the userid
                    os.kill(-1,9)
            
            log('The process has been killed Manually') 
            submission.result = RUN_ABORT
            return submission
        
        
        #The process had exit sucessfully, so find out the result
        
        if os.WIFEXITED(stat) :
            run_messages = run_messages + 'EXIT STATUS: ' + str(os.WEXITSTATUS(stat)) + '<BR />'
        else :
            run_messages = run_messages + 'Improper Exit. <BR \> STD_ERROR_LOG: <BR \>'
        
        temp = open(errorfile)
        lines = temp.readlines()
        for line in lines :
            run_messages = run_messages + line + '<BR \>'
        
        if os.WIFSIGNALED(stat) :
            sig = os.WTERMSIG(stat)
            
            if sig == signal.SIGFPE:
                submission.status = FLOATING_POINT_EXCEPTION
                run_messages = run_messages + 'Floating point Exception.'
            elif sig == signal.SIGXCPU:
                submission.status = TIME_LIMIT_EXCEEDED
                run_messages = run_messages + 'Time Limit Exceeded.'
            elif sig == signal.SIGXFSZ:
                submission.status = OUTPUT_FILE_SIZE
                run_messages = run_messages + 'Output File Size Exceeded.'              
            elif sig == signal.SIGKILL:
                submission.status = MEMORY_LIMIT_EXCEEDED
                run_messages = run_messages + 'Possible Memory Limit Exceeded.'
            elif sig == signal.SIGSEGV:
                submission.status = SEGMENTATION_FAULT
                run_messages = run_messages + 'Segmentation Fault.'
            else :
                submission.status = RUN_ABORT
                run_messages = run_messages + 'UnIdentified Exception Occured.'
            
                
        # Process has produced some output, check and return
        if submission.status == QUEUED :
            check = compare_files(outfile,chkfile)
            submission.status = check
            
            if check == ACCEPTED:
                run_messages = run_messages + 'Accepted.'
                
            elif check == WRONG_ANSWER :
                run_messages = run_messages + 'Wrong Answer.'
                
            elif check == PRESENTATION_ERROR :
                run_messages = run_messages + 'Presentation error, Possible White Space Mismatch.'
                
        submission.result = submission.result + run_messages
        
        # Done with this submission :-)
        return submission
        
            
        
            
    
             
    