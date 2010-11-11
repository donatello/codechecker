from os.path import splitext
import os
import subprocess
import se.secexec
class Evaluate:
    def eval_submission(submission, test_grp, submission_exec):
        """Takes submission and test_grp and returns result_set"""
        tlimit = test_grp["timelimit"]
        mlimit = test_grp["memlimit"]
        maxfilesz = 32 #TODO: for now we fix it at 32M
        jailroot = "jail" #FIXME: Need to lay down the exec env

        #Assumption: each infile would be of the form submission_id.in
        for infile in test_grp["input_files"]:
            #First run submission_exec and then validate output
            outfile = splitext(infile)[0] + ".out" 
            errfile = splitext(infile)[0] + ".err" 
            args = ["--infile=%s" % infile,
                    "--outfile=%s" % outfile,
                    "--errfile=%s" % errfile,
                    "--memlimit=%d" % mlimit,
                    "--timelimit=%d" % tlimit,
                    "--maxfilesz=%d" % maxfilesz,
                    "--executable=%s" % submission_exec,
                    "--euid=%d" % 1002, #TODO: someone needs 
                                        #to send the euid to use here
                    "--jailroot=%s" % jailroot]
            args.insert(0, curdir + "/secexec")
            ret_code = se.secexec.secure_spawn(args) 
            #End of executing the submission_exec
            if test_grp["is_cust_scored"] == True:
                #TODO: run cust_execute via secure_spawn 
                #with appropriate infile and outfile
                pass
            else:
                #TODO: perform a diff 
                check = subprocess.Popen('diff -Bb ' + outfile + ' ' + test_grp["input_file"], shell=True,
                                     stdout=subprocess.PIPE)
                diff_op = check.communicate()[0]
                if diff_op == '':
                    #testcase passed
                    pass
                else:
                    #testcase failed
                    pass


            pass
        pass
    pass
