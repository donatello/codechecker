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
        return child.returncode == 0, out+err     
        
class C_Compile(Compile):
    def __init__(self, config):
        Compile.__init__(self, config)
        self.exec_string = config.config.get("CompileCommands", "C_run")

    def compile(self, submission):
        basename = self.config.runpath + str(submission.pk) 
        write_to_disk(submission.code, basename + ".c")
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
        write_to_disk(submission.code, basename + ".cpp")
        self.compile_cmd = self.config.config.get("CompileCommands", "CPP_compile"
                                             ).replace("%s", basename + ".cpp"
                                                       ).replace("%e", basename + ".exe")
        self.exec_string = self.exec_string.replace("%e", basename + ".exe")    
            
        #compiling the submission
        return Compile.compile(self, submission)

class Python_Compile(Compile):
    def __init__(self, config):
        Compile.__init__(self, config)
        self.exec_string = config.config.get("CompileCommands", "Py_run")

    def compile(self, submission):
        basename = self.config.runpath + str(submission.pk) 
        write_to_disk(submission.code, basename + ".py")
        self.compile_cmd = self.config.config.get("CompileCommands", "Py_compile"
                                                  ).replace("%s", basename + ".py")         
        self.exec_string = self.exec_string.replace("%s", basename + ".py")
            
        #compiling the submission
        return Compile.compile(self, submission)

class Pascal_Compile(Compile):
    def __init__(self, config):
        Compile.__init__(self, config)
        self.exec_string = config.config.get("CompileCommands", "Pascal_run")

    def compile(self, submission):
        basename = self.config.runpath + str(submission.pk) 
        write_to_disk(submission.code, basename + ".p")
        self.compile_cmd = self.config.config.get("CompileCommands", "Pascal_compile"
                                                  ).replace("%s", basename + ".p"
                                                            ).replace("%e", basename + ".exe")
        self.exec_string = self.exec_string.replace("%e", basename + ".exe")    

        #compiling the submission
        return Compile.compile(self, submission)             

class Java_Compile(Compile):
    #Source code is written onto Main.java and the classname is expected to be Main
    def __init__(self, config):
        Compile.__init__(self, config)
        self.exec_string = config.config.get("CompileCommands", "Java_run")

    def compile(self, submission):
        basename = self.config.runpath + str(submission.pk) 
        write_to_disk(submission.code, self.config.runpath + "Main.java")
        self.compile_cmd = self.config.config.get("CompileCommands", "Java_compile"
                                                  ).replace("%s", self.config.runpath + "Main.java")
        self.exec_string = self.exec_string.replace("%c", "Main"
                                                     ).replace("%l", self.config.heapsize+"m"
                                                             ).replace("%p", self.config.runpath)

        #compiling the submission
        return Compile.compile(self, submission)             
