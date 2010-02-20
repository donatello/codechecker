# This file implements SimpleChecker which is just a routine to run a
# user submission against a given test case and report if the result
# to the caller. It does not modify the ranklist or the db. That is
# the work of the caller.

#!/usr/bin/python
import os
import sys
import resource
import string
import datetime
import time
import signal
import subprocess

from codechecker.contests.models import Submission,Problem #,Ranklist
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User

RUNS_PATH = '/tmp/'
OUTPUT_FILE_SIZE = int(64 << 20)    #max 64 MB
HANG_TIME = 1


def log(msg):
    a=open('/tmp/nohup.out','a')
    a.write(msg + '\n')
    return

def run(submission, testcase):
    
    prob = Problem.objects.get(id=submission.problem_id)

    file_root = RUNS_PATH + str(submission.pk)
    
    tlimit = prob.tlimit
    mlimit = prob.mlimit
    
    # Create the input file.    
    infile = str(file_root + '.in')
    f = open(infile, "w")
    f.write(testcase.inputFile)
    f.close()
    
    # Output and error files    
    outfile = str(file_root + '.out')
    errorfile = str(file_root + '.err')
   
    child_id = os.fork()
    if child_id != 0 : # PARENT
        
        time.sleep( prob.tlimit + 1)

        # create reference output file
        chkfile = str(file_root + '.ref')
        f = open(chkfile, "w")
        f.write(testcase.outputFile)
        f.close()
        
        # Reload submission from db here?!
        submission = Submission.objects.get(id = submission.id)

        if submission.result == 'RUN' :
            check = subprocess.Popen('diff -B ' + outfile + ' ' + chkfile, shell=True, 
                                     stdout=subprocess.PIPE)
            diff_op = check.communicate()[0]
            if diff_op == '' :
                log("Testcase #%s matched." % testcase.id)
                return

#                 prob_inst = Problem.objects.get(id=submission.problem_id)
#                 user_inst = User.objects.get(id=submission.user_id)
#                 max_points = prob_inst.points
#                 marks = max_points-find_len(str(submission.code))
#                 if marks < 0 :
#                     marks = 0                 
#                 try :
#                     result = Ranklist.objects.get( 
#                         user = user_inst,
#                         problem = prob_inst,
#                     )
                    
#                     if result.points < marks :
#                         result.points = marks
#                         result.save()
                
#                 except ObjectDoesNotExist:
#                     result = Ranklist.objects.create(
#                         user = user_inst , 
#                         problem = prob_inst,
#                         submission = submission,
#                         points = marks,
#                     )
               
            else :
                submission.result = 'WA'
        
        return
        
    elif child_id == 0 :
                
        instream = open(infile,'r')
        outstream = open(outfile,'w')
        errorstream = open(errorfile,'w')

        exec_file = file_root + '.exe'

        log('Running inside child %s with input file as %s ' % (exec_file,infile))

        tlimit = prob.tlimit
        mlimit = prob.mlimit*1024*1024
        
        #set the time limit for the problem execution
        resource.setrlimit(resource.RLIMIT_CPU,(tlimit,tlimit+1))
            
        #set the output file date size
        resource.setrlimit(resource.RLIMIT_FSIZE,(OUTPUT_FILE_SIZE,OUTPUT_FILE_SIZE))
        
        #set the stack,heap limits
        # resource.setrlimit(resource.RLIMIT_STACK,(mlimit,mlimit))
        # --> no giving extra stack space - leave unmodified. It is 8
        # MB default
        resource.setrlimit(resource.RLIMIT_DATA,(mlimit,mlimit))
              
        #disable forking
        #the 2 process limit get used up any way !
        #resource.setrlimit(resource.RLIMIT_NPROC,(2,2))
        
        #file limit

        # Create childprocess as setuid_helper and pass the executable
        # to it.
        helper_child = subprocess.Popen("./setuid_helper %s" % (exec_file,),
                                        shell = True,
                                        stdin = subprocess.PIPE,
                                        stdout = subprocess.PIPE,
                                        stderr = subprocess.PIPE)
        
        
        try :
            helper_out = helper_child.communicate(instream.read())
            
            log("Child execution terminated\n")
        
            if helper_child.returncode < 0  :
                log('Code execution failed with exit status: ' 
                    + str(helper_child.returncode) + ' \n')
                outstream.write(str(helper_out[0]) )
                errorstream.write(str(helper_out[1]))
                sig = - helper_child.returncode

                
                if sig == signal.SIGXCPU :
                    submission.result = 'TLE'
                    
                elif sig == signal.SIGXFSZ :
                    submission.result = 'OUTE'
                    
                elif sig == signal.SIGSEGV :
                    submission.result = 'SEG'
                
                elif sig == signal.SIGFPE :
                    submission.result = 'FPE'
                
                elif sig == signal.SIGKILL :
                    submission.result = 'MLE'
                
                elif sig == signal.SIGABRT :
                    submission.result = 'ABRT'
                
                else :                    
                    submission.result = 'UNKN'

                submission.save()
                outstream.close()
                errorstream.close()
            elif helper_child.returncode == 0 :
                log('Code execution successful with exit status 0')
                
                outstream.write(str(helper_out[0]) )
                errorstream.write(str(helper_out[1]))

            outstream.close()
            errorstream.close()
        except :
            log('Unknown exception!')
            log('Code Termination Failed !\n')
            log('Comments : \n' + str(sys.exc_info()[0]) + str(sys.exc_info()[1]) )
            submission.result = 'UNKN'
            submission.save()
        
        os._exit(0)
    
