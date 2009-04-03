import os
import sys
import time
import string

from contests.models import Submission,Problem
import SimpleChecker
import MultipleChecker
import ComplexChecker

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


def handle_submission( submission ):
    # sub_instance is the db field for the submission        
    sub_instance = Submission.objects.get(ID=submission['ID'])
    code = sub_instance.code
    f = open(RUNS_PATH + str(sub_instance.ID) + '.' + sub_instance.lang,'w')
    f.write(code)
    f.close()
    # generate the compile command for the submission
    submission['cmd'] = generate_compile_command( submission )
    
    # compile the file 
    sub_instance.result = 'CMP'
    sub_instance.save()
    
    compiler_out = os.popen(submission['cmd'])
    comments=compiler_out.read()
    log(comments)
    
    # If compilation successful then proceed
    
    if os.path.exists(RUNS_PATH + str(sub_instance.ID) + '.exe') == 0 :
    #if len(comments) != 0 :
        sub_instance.result = 'CMPE'
        sub_instance.save()
        return
       
    comments = comments + "Compilation Successful \n"
    log("Compilation Successful for submission #%s" % str(submission['ID']))
    sub_instance.result = 'RUN'
    sub_instance.save()
        
    prob = Problem.objects.get(ID=submission['problem'])
    
    # Log for debug purposes
#    for key,val in submission.iteritems():
#        log( key + ' : ' + str(val) )
    
    if prob.ptype == 'Simple' :
        SimpleChecker.run(submission)
        
    elif prob.ptype == 'Multiple' :
        MultipleChecker.run(submission)
    elif prob.ptype == 'Complex' :
        ComplexChecker.run(submission)
    
    return
    
    
    
    
