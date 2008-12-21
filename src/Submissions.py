#!/usr/bin/python
import os
import string

from Globals import *
from DbConnect import *
import SingleFileChecker
import MultipleFileChecker

def compile_command(a):
    s = str('')
    if a.lang == 'C++':
        s = 'g++ -o -Wall ' + RUNS_PATH + str(a.id)  + '.out ' + str(a.file)
    elif a.lang == 'C':
        s = 'gcc -Wall -lm -o ' + RUNS_PATH + str(a.id)  + '.out ' + str(a.file)
    elif a.lang == 'JAVA':
        s = 'do nothing for now '
    log(s)
    return s


def HandleSubmission( submission ):
       
    # get the correct Compilation language
    cmd = compile_command(submission)
    
    # compile the file using the cmd and then append the Compiler 
    db.updateSubmissions(submission, "Compiling")
    compiler_out = os.popen(cmd)
    comments = str()
    temps = compiler_out.readlines()
    for temp in temps:
        comments = comments + temp + "<br \>"
    
    # If compilation successful then proceed

    if len(comments) != 0 :
        submission.compile_error = comments
        return COMPILE_ERROR
    
    comments = comments + "Compilation Successful <br \>"
    
    log("Compilation Successful for submission #%s" % str(submission.id))
    
    result = str()
    
    # Run the test cases
    
    ptype = db.getProblemType(submission.pid)
    
    if ptype == 'single' :
        result = SingleFileChecker.run(submission)
    elif ptype == 'multiple' :
        result = MultipleFileChecker.run(submission)
    else :
        result = 'The judge cannot check this type of problems yet';
    
    return result
