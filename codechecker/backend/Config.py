import ConfigParser
import os

class Config:
    config = None
    
    def __init__(self):
        config = ConfigParser.ConfigParser()
        config.read("utils/codechecker.conf")
        #print config.sections()
        self.runpath = config.get("BackendMain", "RunsPath")
        self.outputLimit = int(config.get("BackendMain","OutputFileSizeLimit"))
        
        # Check if setuid_helper exists.
        self.shPath = config.get("BackendMain", "CheckerRoot") + "codechecker/backend/setuid_helper"
        assert os.path.isfile(self.shPath) and os.access(self.shPath, os.X_OK)
        

if __name__ == "__main__":
    
    config = Config()
    

