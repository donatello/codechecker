# This class has methods to run each test against the submission and
# evaluate correctness.

from codechecker.contests.models import Submission, Problem, Testcase, TestSet, Contest, TestcaseEval
from misc_utils import write_to_disk
from codechecker.Logger import *
import os, stat, subprocess, sys, signal

class TestsRunner:
    
    def __init__(self, config, compile, submission):
        self.config = config
        self.compile = compile
        self.submission = submission
        self.infile = self.outfile = self.errfile = self.chkfile = None
        self.log = Logger(__file__, config.config.get("BackendMain", "LogFile")).log

    # Main function for this class. Finds all testcases for this
    # submission and calls test() and evaluate() on each of them.
    def run_tests(self):
        self.submission.result = "RUN"
        self.submission.save()

        testsets = TestSet.objects.filter(problem = self.submission.problem)
        for testset in testsets:
            all_testcases = Testcase.objects.filter(testSet = testset)
            finish_testing = False
            for testcase in all_testcases:
                status = self.test(testcase)                
                testEval = TestcaseEval()
                testEval.submission = self.submission
                testEval.testcase = testcase
                if status == "RUN":
                    test_status = self.evaluate(testcase)

                    print "test_status: ", test_status
                    testEval.pass_status = test_status["STATUS"]
                    testEval.save()
                else:
                    testEval.pass_status = status
                    testEval.save()

                    self.submission.result = status
                    self.submission.save()
                    finish_testing = True                
                    break

            if finish_testing: break

    # Runs the submission against a testcase
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

        self.log('Running executable %s with input file as %s' 
            % (self.compile.exec_string, self.infile), Logger.DEBUG)

        # Call setuid_helper to execute the child
        helper_child = subprocess.Popen([self.config.shPath, 
                                         "--debug=%s" % str(Logger.DEBUG),
                                         "--infile=%s" % self.infile,
                                         "--outfile=%s" % self.outfile,
                                         "--errfile=%s" % self.errfile,
                                         "--memlimit=%d" % mlimit,
                                         "--timelimit=%d" % tlimit,
                                         "--maxfilesz=%d" % self.config.outputLimit]
                                        + self.compile.exec_string.split())
        
        try:
            
            helper_child.communicate()

            retval = self.process_returncode(helper_child.returncode)

            #self.log("Setting submission status to %s" % retval, Logger.DEBUG)
            #self.submission.result = retval
            #self.submission.save()

            return retval

        except :
            self.log('Unknown exception. setuid_helper died on us! Comments : \n' +
                str(sys.exc_info()[0]) + str(sys.exc_info()[1]), Logger.DEBUG)
            #self.submission.result = 'WTF'
            #self.submission.save()
            sys.exit(1)

    def process_returncode(self, returncode):
        self.log("[return code processing debug output STARTS]", Logger.DEBUG)
        self.log("RETURN CODE = %d" % returncode, Logger.DEBUG)

        #check for the magic condition that tells that execvp
        #failed in the setuid program
        if returncode == 111:
            self.log('EXECVE failed in the child!! Exiting NOW!', Logger.DEBUG)
            os._exit(0)

        retval = ""

        if returncode > 0:
            self.log('Code execution FAILED!', Logger.DEBUG)

            if returncode == signal.SIGXCPU:
                retval = 'TLE'

            elif returncode == signal.SIGXFSZ:
                retval = 'OUTE'

            elif returncode == signal.SIGSEGV:
                retval = 'SEG'

            elif returncode == signal.SIGFPE:
                retval = 'FPE'

            elif returncode == signal.SIGKILL:
                retval = 'KILL'

            elif returncode == signal.SIGABRT:
                retval = 'ABRT'

            else:                    
                retval = 'RTE'

            self.log('retval = %s' % retval, Logger.DEBUG)
        elif returncode == 0:
            retval = "RUN"
            self.log('Execution successful with exit status 0', Logger.DEBUG)
            
        self.log('[return code processing debug output ENDS]', Logger.DEBUG)
        return retval
         
    # Evaluates the result of a run against a testcase.
    def evaluate(self, testcase, test_result = None):

        # Reload submission from db here?!
        # self.submission = Submission.objects.get(id = submission.id)

        if self.submission.result == 'RUN' :

            #Decide how to evaluate based on if a setter binary is
            #given for this problem:
            prob = Problem.objects.get(id = self.submission.problem_id)
            ret_status = {}            
            if prob.cust_eval != "":
                print "APPROX PROBLEM"

                #Is an approximate problem. Evaluate using cust_eval

                #TODO: Complete this stub.

                pass
            else: #not approximate, use default diff method.
                print "NON-APPROX PROBLEM"
                # create reference output file
                self.chkfile = self.config.runpath + '.ref'
                write_to_disk(testcase.output.
                              replace('\r\n','\n'), # Replace windows
                                                    # newline with linux
                                                    # newline
                              self.chkfile) 
                check = subprocess.Popen('diff -Bb ' + self.outfile + ' ' + self.chkfile, shell=True,
                                         stdout=subprocess.PIPE)
                diff_op = check.communicate()[0]
                if diff_op == '':
                    self.log("Testcase #%s was CORRECTLY answered!" % testcase.id, Logger.DEBUG)
                    print "Testcase #%s was CORRECTLY answered!" % testcase.id
                    ret_status["STATUS"] = "PASSED"                    
                else:
                    #self.submission.result = 'WA'
                    #self.submission.save()
                    ret_status["STATUS"] = "FAILED"

            return ret_status

        # Cleaning up test case reference output, input, output and
        # error files.
        #os.remove(self.chkfile)
        #os.remove(self.infile)
        #os.remove(self.outfile)
        #os.remove(self.errorfile)

        return self.submission.result == "RUN"
