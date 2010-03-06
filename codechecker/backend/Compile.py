# This class compiles a submission. Has extensible support for
# multiple languages.

class Compile:
    
    def __init__(self, config):
        self.config = config

    # Returns a (Bool, String), where the bool represents success of
    # compilation, and String represents compiler stdout/err.
    def compile(self, submission):
        pass
    
