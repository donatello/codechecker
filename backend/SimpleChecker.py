#!/usr/bin/python
import os
import sys
import resource
import string
import datetime
import time
import signal
import subprocess

from contests.models import Submission,Problem,Ranklist
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User

RUNS_PATH = '/share/data/submissions/'
PROBLEM_PATH = '/share/data/problems/'
OUTPUT_FILE_SIZE = int(64 << 20)    #max 64 MB
HANG_TIME = 1


def log(msg):
    a=open('/share/checker/nohup.out','a')
    a.write(msg + '\n')
    return


def execute(submission):
    pass


def find_len(code):
    l = 0
    for i in range(len(code)) :
        if code[i] != ' ' and code[i] != '\n' :
            l = l + 1
    
    return l

def run(submission):
    
    prob = Problem.objects.get(ID=submission['problem'])
    sub_instance = Submission.objects.get(ID=submission['ID'])

    file_root = RUNS_PATH + str(submission['ID'])
    
    tlimit = prob.tlimit
    mlimit = prob.mlimit
    
    
    infile = str(PROBLEM_PATH + prob.pcode + '/infile')
    chkfile = str(PROBLEM_PATH + prob.pcode + '/outfile')
    outfile = str(file_root + '.out')
    errorfile = str(file_root + '.err')
   
    child_id = os.fork()
    if child_id != 0 :
        
        time.sleep( prob.tlimit + 1)
        sub_instance = Submission.objects.get(ID=submission['ID'])
        
        if sub_instance.result == 'RUN' :
            check = os.popen('diff -B '+ outfile + ' '+ chkfile)
            if check.read() == '' :
                sub_instance.result = 'ACC'
                prob_inst = Problem.objects.get(ID=sub_instance.problem_id)
                user_inst = User.objects.get(id=sub_instance.user_id)
                max_points = prob_inst.points
                marks = max_points-find_len(str(sub_instance.code))
                if marks < 0 :
                    marks = 0                 
                try :
                    result = Ranklist.objects.get( 
                        user = user_inst,
                        problem = prob_inst,
                    )
                    
                    if result.points < marks :
                        result.points = marks
                        result.save()
                
                except ObjectDoesNotExist:
                    result = Ranklist.objects.create(
                        user = user_inst , 
                        problem = prob_inst,
                        submission = sub_instance,
                        points = marks,
                    )
               
            else :
                sub_instance.result = 'WA'
        
        sub_instance.save()
        return
        
    if child_id == 0 :
        
        os.setuid(7500+int( time.time() )%100007)

        instream = open(infile,'r')
        outstream = open(outfile,'w')
        errorstream = open(errorfile,'w')

        exec_file = file_root + '.exe'

        log('Running inside child %s with input file as %s ' % (exec_file,infile))

        tlimit = prob.tlimit
        mlimit = prob.mlimit
        
        #set the time limit for the problem execution
        resource.setrlimit(resource.RLIMIT_CPU,(tlimit,tlimit+1))
            
        #set the output file date size
        resource.setrlimit(resource.RLIMIT_FSIZE,(OUTPUT_FILE_SIZE,OUTPUT_FILE_SIZE))
        
        #set the stack,heap limits
        resource.setrlimit(resource.RLIMIT_STACK,(mlimit,mlimit))
        resource.setrlimit(resource.RLIMIT_DATA,(mlimit,mlimit))
              
        #disable forking
        #the 2 process limit get used up any way !
        resource.setrlimit(resource.RLIMIT_NPROC,(2,2))
        
        #file limit
        
        
                        
        # new subprocess for the submission
        child = subprocess.Popen(exec_file, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False, )
        
        
        try :
            
            if child.stdin :
                child.stdin.write(instream.read())
        
            out = child.communicate()

            if child.returncode == None :
                os.kill(child.pid,9)
                sub_instance.result = 'FRK'
                sub.save()
                os._exit(0)
        
            elif child.returncode < 0  :
                log('Code execution failed with exit status: ' + str(child.returncode) + ' \n')
                outstream.write('' + str(out[0]) )
                errorstream.write('' + str(out[1]))
                sig = - child.returncode

                
                if sig == signal.SIGXCPU :
                    sub_instance.result = 'TLE'
                    
                elif sig == signal.SIGXFSZ :
                    sub_instance.result = 'OUTE'
                    
                elif sig == signal.SIGSEGV :
                    sub_instance.result = 'SEG'
                
                elif sig == signal.SIGFPE :
                    sub_instance.result = 'FPE'
                
                elif sig == signal.SIGKILL :
                    sub_instance.result = 'MLE'
                
                elif sig == signal.SIGABRT :
                    sub_instance.result = 'ABRT'
                    
                
                
                else :
                    sub_instance.result = 'UNKN'
                
                sub_instance.save()
                outstream.close()
                errorstream.close()
                os._exit(0)
            elif child.returncode == 0 :
                log('Code execution successful with exit status 0')
                
                outstream.write('' + str(out[0]))
                errorstream.write('' + str(out[1]))
                outstream.close()
                errorstream.close()
                os._exit(0)            
        except :
            log('Code Termination Failed !\n')
            log('Comments : \n' + str(sys.exc_info()[0]) + str(sys.exc_info()[1]) )
            sub_instance.result = 'UNKN'
            sub_instance.save()
        
        
        os._exit(0)
    
