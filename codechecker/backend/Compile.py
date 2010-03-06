# This class compiles a submission. Has extensible support for
# multiple languages.

import subprocess

class Compile:
    
    def __init__(self, config):
        self.config = config
        self.compile_cmd = self.exec_string = None

    # Returns a (Bool, String), where the bool represents success of
    # compilation, and String represents compiler stdout/err.
    def compile(self, submission):
        child = subprocess.Popen(self.compile_cmd, stdout = subprocess.PIPE, 
                            stderr = subprocess.PIPE)
        out, err = child.communicate()
        return child.returncode == 0, err     
    
    def _write_to_disk(self, text, filename):
        f = file(filename, "w")
        f.write(text)
        f.close()
    
class C_Compile(Compile):
    def __init__(self, config):
        Compile(self, config)
        self.exec_string = config.config.get("CompileCommands", "C_run")

    def compile(self, submission):
        basename = self.config.runpath + str(submission.pk) 
        self._write_to_disk(submission.submissionCode, basename + ".c")
        self.compile_cmd = config.config.get("CompileCommands", "C_compile").
                                                replace("%s", basename + ".c").
                                                replace("%e", basename + ".exe")
            
        #compiling the submission
        return Compile.compile()
             
         
    
class CPP_Compile(Compile):
    def __init__(self, config):
        Compile(self, config)
        self.exec_string = config.config.get("CompileCommands", "CPP_run")

    def compile(self, submission):
        basename = self.config.runpath + str(submission.pk) 
        self._write_to_disk(submission.submissionCode, basename + ".cpp")
        self.compile_cmd = config.config.get("CompileCommands", "CPP_compile").
                                                replace("%s", basename + ".cpp").
                                                replace("%e", basename + ".exe")
            
        #compiling the submission
        return Compile.compile()
