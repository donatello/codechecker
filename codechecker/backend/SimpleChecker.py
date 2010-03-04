# This file implements SimpleChecker which is just a routine to run a
# user submission against a given test case and report if the result
# to the caller. 

#!/usr/bin/python
import os, stat, signal
import sys
import resource
import string
import datetime
import time
import subprocess

from codechecker.contests.models import Submission,Problem #,Ranklist
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from codechecker.Logger import *

class SimpleChecker:
    config = None
    
    def __init__(self, config):
        self.config = config

    def run(self, submission, testcase):

        prob = Problem.objects.get(id=submission.problem_id)

        file_root = self.config.runpath + str(submission.pk)
        exec_file = self.config.runpath + str(submission.pk) + ".exe"
        print "exec_file = ", exec_file

        # Create the input file.    
        infile = str(file_root + '.in')
        f = open(infile, "w")
        f.write(testcase.inputFile)
        f.close()

        # Output and error files    
        outfile = str(file_root + '.out')
        errorfile = str(file_root + '.err')

        instream = open(infile,'r')        
        outstream = open(outfile,'w')
        os.chmod(outfile, stat.S_IRUSR | stat.S_IWUSR | stat.S_IWOTH | stat.S_IROTH)
        errorstream = open(errorfile,'w')
        os.chmod(errorfile, stat.S_IRUSR | stat.S_IWUSR | stat.S_IWOTH | stat.S_IROTH)

        log('Running in executable %s with input file as %s ' % (exec_file,infile))

        tlimit = prob.tlimit
        mlimit = prob.mlimit

        # Create childprocess as setuid_helper and pass the executable
        # to it along with the file descriptors for the streams. This
        # will let the OS handle buffering of I/O.
        helper_child = subprocess.Popen(["/opt/checker/codechecker/backend/setuid_helper", 
                                         "debug=%s" % str(get_log_level()),
                                         "memlimit=%d" % mlimit,
                                         "timelimit=%d" % tlimit,
                                         "maxfilesize=%d" % self.config.outputLimit,
                                         exec_file],
                                        stdin = instream,
                                        stdout = outstream,
                                        stderr = errorstream)


        try :

            #This will wait for process to terminate
            helper_child.communicate()

            log("return code for helper_child = %d" % helper_child.returncode) 

            #check for the magic condition that tells that execvp
            #failed in the setuid program
            if helper_child.returncode == 111:
                log('EXECVE failed in the child!!!!')
                os._exit(0)

            if helper_child.returncode > 0:
                log('Code execution failed with exit status: ' 
                    + str(helper_child.returncode) + ' \n')
                sig = helper_child.returncode


                if sig == signal.SIGXCPU :
                    submission.result = 'TLE'

                elif sig == signal.SIGXFSZ :
                    submission.result = 'OUTE'

                elif sig == signal.SIGSEGV :
                    submission.result = 'SEG'

                elif sig == signal.SIGFPE :
                    submission.result = 'FPE'

                elif sig == signal.SIGKILL :
                    submission.result = 'KILL'

                elif sig == signal.SIGABRT :
                    submission.result = 'ABRT'

                else :                    
                    submission.result = 'UNKN'

                log('submission result = %s' % submission.result)
                submission.save()
            elif helper_child.returncode == 0 :
                log('Code execution successful with exit status 0')

        except :
            log('Unknown exception. setuid_helper died on us! Comments : \n' + 
                str(sys.exc_info()[0]) + str(sys.exc_info()[1]) )
            submission.result = 'WTF'
            submission.save()

        # create reference output file
        chkfile = str(file_root + '.ref')
        f = open(chkfile, "w")
        f.write(testcase.outputFile)
        f.close()

        # fixes the dos format of ref files (caused because of MySQL?!)
        fromdos_ret = subprocess.call(["fromdos",chkfile])
        #print "Return code", fromdos_ret

        # Reload submission from db here?!
        submission = Submission.objects.get(id = submission.id)

        if submission.result == 'RUN' :
            check = subprocess.Popen('diff -Bb ' + outfile + ' ' + chkfile, shell=True, 
                                     stdout=subprocess.PIPE)
            diff_op = check.communicate()[0]
            if diff_op == '' :
                log("Testcase #%s matched." % testcase.id)

            else :
                submission.result = 'WA'
                submission.save()

        # Cleaning up test case reference output, input, output and
        # error files.
        #os.remove(chkfile)
        #os.remove(infile)
        #os.remove(outfile)
        #os.remove(errorfile)

        return
