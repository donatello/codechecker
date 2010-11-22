import ConfigParser
import os

class Config:
    
    def __init__(self, configFilePath):
        self.config = ConfigParser.ConfigParser()
        self.config.read(configFilePath)
        self.jail_root = self.config.get("BackendMain","JailRoot")
        runs_path = self.config.get("BackendMain", "RunsPath")
        self.runpath = os.path.join('/' , runs_path)
        self.abs_path = os.path.join(self.jail_root, runs_path)
        self.outputLimit = int(self.config.get("BackendMain","OutputFileSizeLimit"))
        self.heapsize = self.config.get("RuntimeLimits", "HeapSize")
        
        # Check if setuid_helper exists.
        self.shPath = self.config.get("BackendMain", "CheckerRoot") + "codechecker/backend/setuid_helper"
        assert os.path.isfile(self.shPath) and os.access(self.shPath, os.X_OK)
        

if __name__ == "__main__":
    
    config = Config("conf/codechecker.conf")
    print config.config.sections()
    print config.config.get("CompileCommands", "C_compile")
    

