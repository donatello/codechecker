import ConfigParser
import os

class Config:
    
    def __init__(self):
        self.config = ConfigParser.ConfigParser()
        self.config.read("utils/codechecker.conf")
        self.runpath = self.config.get("BackendMain", "RunsPath")
        self.outputLimit = int(self.config.get("BackendMain","OutputFileSizeLimit"))
        self.heapsize = self.config.get("RuntimeLimits", "HeapSize")
        
        # Check if setuid_helper exists.
        self.shPath = self.config.get("BackendMain", "CheckerRoot") + "codechecker/backend/setuid_helper"
        assert os.path.isfile(self.shPath) and os.access(self.shPath, os.X_OK)
        

if __name__ == "__main__":
    
    config = Config()
    print config.config.sections()
    print config.config.get("CompileCommands", "C_compile")
    

