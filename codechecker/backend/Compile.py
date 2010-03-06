# This class compiles a submission. Has extensible support for
# multiple languages.

import subprocess
from misc_utils import write_to_disk

class Compile:
    
    def __init__(self, config):
        self.config = config
        self.compile_cmd = self.exec_string = None

    # Returns a (Bool, String), where the bool represents success of
    # compilation, and String represents compiler stdout/err.
    def compile(self, submission):
        print self.compile_cmd
        child = subprocess.Popen(self.compile_cmd, stdout = subprocess.PIPE, 
                                 stderr = subprocess.PIPE, shell=True)
        out, err = child.communicate()
        return child.returncode == 0, err     
        
class C_Compile(Compile):
    def __init__(self, config):
        Compile.__init__(self, config)
        self.exec_string = config.config.get("CompileCommands", "C_run")

    def compile(self, submission):
        basename = self.config.runpath + str(submission.pk) 
        write_to_disk(submission.submissionCode, basename + ".c")
        self.compile_cmd = self.config.config.get("CompileCommands", "C_compile"
                                                  ).replace("%s", basename + ".c"
                                                            ).replace("%e", basename + ".exe")
        self.exec_string = self.exec_string.replace("%e", basename + ".exe")    

        #compiling the submission
        return Compile.compile(self, submission)             

    
class CPP_Compile(Compile):
    def __init__(self, config):
        Compile.__init__(self, config)
        self.exec_string = config.config.get("CompileCommands", "CPP_run")

    def compile(self, submission):
        basename = self.config.runpath + str(submission.pk) 
        write_to_disk(submission.submissionCode, basename + ".cpp")
        self.compile_cmd = self.config.config.get("CompileCommands", "CPP_compile"
                                             ).replace("%s", basename + ".cpp"
                                                       ).replace("%e", basename + ".exe")
        self.exec_string = self.exec_string.replace("%e", basename + ".exe")    
            
        #compiling the submission
        return Compile.compile(self, submission)
