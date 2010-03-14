# This class has methods to run each test against the submission and
# evaluate correctness.

from codechecker.contests.models import Submission, Problem, Testcase, TestSet, Contest
from misc_utils import write_to_disk
from codechecker.Logger import *
import os, stat, subprocess, sys, signal

class TestsRunner:
    
    def __init__(self, config, compile, submission):
        self.config = config
        self.compile = compile
        self.submission = submission
        self.infile = self.outfile = self.errfile = self.chkfile = None

    # Main function for this class. Finds all testcases for this
    # submission and calls test() and evaluate() on each of them.
    def run_tests(self):
        self.submission.result = "RUN"
        self.submission.save()

        testsets = TestSet.objects.filter(problem = self.submission.problem)
        for testset in testsets:
            all_testcases = Testcase.objects.filter(testSet = testset)
            to_break = False
            for testcase in all_testcases:
                self.test(testcase)                
                res = self.evaluate(testcase)
                if not res:
                    to_break = True
                    break
            if to_break: break

        if self.submission.result == "RUN":
            self.submission.result = "ACC"
            self.submission.save()

    # Runs the submission against a testcase.
    def test(self, testcase):

        # create input file
        self.infile = self.config.runpath + str(self.submission.pk) + ".in"
        write_to_disk(testcase.input, self.infile)
        
        # create output and error files and allow "others" to write
        self.outfile = self.config.runpath + str(self.submission.pk) + ".out"
        write_to_disk("", self.outfile)
        self.errfile = self.config.runpath + str(self.submission.pk) + ".err"
        write_to_disk("", self.errfile)
        os.chmod(self.outfile, stat.S_IRUSR | stat.S_IWUSR | stat.S_IWOTH | stat.S_IROTH)
        os.chmod(self.errfile, stat.S_IRUSR | stat.S_IWUSR | stat.S_IWOTH | stat.S_IROTH)

        # Get problem specific limits
        prob = Problem.objects.get(id = self.submission.problem_id)
        tlimit = prob.tlimit
        mlimit = prob.mlimit

        log('Running executable %s with input file as %s' 
            % (self.compile.exec_string, self.infile))

        # Call setuid_helper to execute the child
        helper_child = subprocess.Popen([self.config.shPath, 
                                         "debug=%s" % str(get_log_level()),
                                         "infile=%s" % self.infile,
                                         "outfile=%s" % self.outfile,
                                         "errfile=%s" % self.errfile,
                                         "memlimit=%d" % mlimit,
                                         "timelimit=%d" % tlimit,
                                         "maxfilesize=%d" % self.config.outputLimit,
                                         self.compile.exec_string])
        
        try:
            
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
                    self.submission.result = 'TLE'

                elif sig == signal.SIGXFSZ :
                    self.submission.result = 'OUTE'

                elif sig == signal.SIGSEGV :
                    self.submission.result = 'SEG'

                elif sig == signal.SIGFPE :
                    self.submission.result = 'FPE'

                elif sig == signal.SIGKILL :
                    self.submission.result = 'KILL'

                elif sig == signal.SIGABRT :
                    self.submission.result = 'ABRT'

                else :                    
                    self.submission.result = 'UNKN'

                log('submission result = %s' % self.submission.result)
                self.submission.save()
            elif helper_child.returncode == 0 :
                log('Code execution successful with exit status 0')

        except :
            log('Unknown exception. setuid_helper died on us! Comments : \n' +
                str(sys.exc_info()[0]) + str(sys.exc_info()[1]) )
            self.submission.result = 'WTF'
            self.submission.save()

         
    # Evaluates the result of a run against a testcase.
    def evaluate(self, testcase, test_result = None):

        # Reload submission from db here?!
        # self.submission = Submission.objects.get(id = submission.id)

        if self.submission.result == 'RUN' :
            # create reference output file
            self.chkfile = self.config.runpath + '.ref'
            write_to_disk(testcase.output.
                          replace('\r\n','\n'), # Replace windows
                                                # newline with linux
                                                # newline
                          self.chkfile) 

            # check the diff
            check = subprocess.Popen('diff -Bb ' + self.outfile + ' ' + self.chkfile, shell=True,
                                     stdout=subprocess.PIPE)
            diff_op = check.communicate()[0]
            if diff_op == '' :
                log("Testcase #%s output matched." % testcase.id)

            else :
                self.submission.result = 'WA'
                self.submission.save()

        # Cleaning up test case reference output, input, output and
        # error files.
        #os.remove(self.chkfile)
        #os.remove(self.infile)
        #os.remove(self.outfile)
        #os.remove(self.errorfile)

        return self.submission.result == "RUN"
