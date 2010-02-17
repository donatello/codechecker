import os
import sys
import time
import string

from contests.models import Submission,Problem
import SimpleChecker
#import MultipleChecker
#import ComplexChecker

RUNS_PATH = '/share/data/submissions/'

def log(msg):
    a=open('/share/checker/nohup.out','a')
    a.write(msg + '\n')
    return

def generate_compile_command(sub):
    s = str('')
    file_root = RUNS_PATH + str(sub['ID']) 
    
    if sub['lang'] == 'cpp':
        s = 'g++  -o '+ str(file_root)  + '.exe ' + str(str(file_root) + '.' + sub['lang'])
    elif sub['lang'] == 'c':
        s = 'gcc  -o ' + str(file_root)  + '.exe ' + str(str(file_root) + '.' + sub['lang'])
    elif sub['lang'] == 'java':
        s = 'do nothing for now '
    return s


# The 'submission' argument is a model-instance (not a dictionary).
def handle_submission( submission ):

    #write the submission code to a file.
    submission.write_code_to_disk()

    # compile the submission
    compiler_out = submission.compile()

    # check the compile result.
    if not(submission.check_compile_result()):
        return

    # Compilation is successful. So proceeding.
       
    compilation_out += "Compilation Successful\n"
    log("Compilation Successful for submission #%s" % str(submission['ID']))

    # Run the submission's generated executable.
    prob = Problem.objects.get(ID=submission.problem)
    submission.execute(prob)
    
    if prob.ptype == 'Simple' :
        SimpleChecker.run(submission)
        
    elif prob.ptype == 'Multiple' :
        MultipleChecker.run(submission)
    elif prob.ptype == 'Complex' :
        ComplexChecker.run(submission)
    
    return
    
