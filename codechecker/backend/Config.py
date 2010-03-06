import ConfigParser

class Config:
    config = None
    
    def __init__(self):
        config = ConfigParser.ConfigParser()
        config.read("utils/codechecker.conf")
        #print config.sections()
        self.runpath = config.get("BackendMain", "RunsPath")
        self.outputLimit = int(config.get("BackendMain","OutputFileSizeLimit"))

if __name__ == "__main__":
    
    config = Config()
    

