# This class compiles a submission. Has extensible support for
# multiple languages.

import subprocess
from misc_utils import write_to_disk
import os.path

class Compile:
    
    def __init__(self, config, submission):
        self.config = config
        self.submission = submission
        
        #set compile command and exec command to None, they will be set by the,
        self.compile_cmd = None
        self.exec_string = None
        
        #get the basename
        self.basename = os.path.join(self.config.runpath , str(submission.pk))
        #write the code to the file
        #the java submission file will also be created here but only Main.java
        #created in Java_Compile would be compiled and run. 
        write_to_disk(submission.code, self.basename + '.' + str(submission.language))
        
        
    # Returns a (Bool, String), where the bool represents success of
    # compilation, and String represents compiler stdout/err.
    def compile(self):
        print self.compile_cmd
        child = subprocess.Popen(self.compile_cmd, stdout = subprocess.PIPE, 
                                 stderr = subprocess.PIPE, shell=True)
        out, err = child.communicate()
        return child.returncode == 0, out+err     
        
class C_Compile(Compile):
    def __init__(self, config, submission):
        Compile.__init__(self, config, submission)
        self.compile_cmd = config.config.get("CompileCommands", "C_compile")
        self.exec_string = config.config.get("CompileCommands", "C_run")

    def compile(self):

        self.compile_cmd = self.compile_cmd.replace("%s", self.basename + '.c'
                                    ).replace("%e", self.basename + '.exe')
                                    
        self.exec_string = self.exec_string.replace("%e", self.basename + '.exe')    

        #compiling the submission
        return Compile.compile(self)             

    
class CPP_Compile(Compile):
    def __init__(self, config, submission):
        Compile.__init__(self, config, submission)
        self.compile_cmd = config.config.get("CompileCommands", "CPP_compile")
        self.exec_string = config.config.get("CompileCommands", "CPP_run")
    
    def compile(self):
        
        self.compile_cmd = self.compile_cmd.replace("%s", self.basename + '.cc'
                                    ).replace("%e", self.basename + '.exe')
                                    
        self.exec_string = self.exec_string.replace("%e", self.basename + '.exe')    
            
        #compiling the submission
        return Compile.compile(self)

class Python_Compile(Compile):
    def __init__(self, config, submission):
        Compile.__init__(self, config, submission)
        self.compile_cmd = config.config.get("CompileCommands", "Py_compile")
        self.exec_string = config.config.get("CompileCommands", "Py_run")

    def compile(self): 
        
        self.compile_cmd = self.compile_cmd.replace("%s", self.basename + '.py')         
        self.exec_string = self.exec_string.replace("%s", self.basename + '.py')
            
        #compiling the submission
        return Compile.compile(self)

class Pascal_Compile(Compile):
    def __init__(self, config):
        Compile.__init__(self, config)
        self.compile_cmd = config.config.get("CompileCommands", "Pascal_compile")
        self.exec_string = config.config.get("CompileCommands", "Pascal_run")

    def compile(self): 
        
        self.compile_cmd = self.compile_cmd.replace("%s", self.basename + '.p'
                                    ).replace("%e", self.basename + '.exe')
                                    
        self.exec_string = self.exec_string.replace("%e", self.basename + '.exe')    

        #compiling the submission
        return Compile.compile(self)             

class Java_Compile(Compile):
    #Source code is written onto Main.java and the classname is expected to be Main
    def __init__(self, config, submission):
        Compile.__init__(self, config, submission)
        self.exec_string = config.config.get("CompileCommands", "Java_run")

    def compile(self): 
        write_to_disk(self.submission.code, self.config.runpath + "Main.java")
        self.compile_cmd = self.config.config.get("CompileCommands", "Java_compile"
                                                  ).replace("%s", self.config.runpath + "Main.java")
        self.exec_string = self.exec_string.replace("%c", "Main"
                                                     ).replace("%l", self.config.heapsize+"m"
                                                             ).replace("%p", self.config.runpath)

        #compiling the submission
        return Compile.compile(self)             
