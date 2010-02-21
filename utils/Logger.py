class Logger:
  def __init__(self, log_level = 0, fname = "/tmp/nohup.out"):
    LOG_LEVEL = log_level
    LOG_FILE = fname 

  def log(self, message):
    f = file(LOG_FILE, "a")
    f.write(message + "\n")
    f.close()
    
