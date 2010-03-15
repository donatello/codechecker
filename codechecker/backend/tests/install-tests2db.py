import sys, os
import datetime
sys.path.append("/opt/checker")
from codechecker.contests.models import Submission, User, Problem

def submit_to_db(files):
    lang_dict = {'C' : "c", 'CPP' : "cpp", "PY" : "py"}
    for fname in files:
      ext = fname.rsplit(".", 1)[1]
      sub = Submission()
      sub.user = User.objects.get(id = 1)
      sub.problem = Problem.objects.get(id = 1) 
      sub.result = "QU"
      sub.time = datetime.datetime.now() 
      sub.language = lang_dict[ext.upper()]
      sub.penalty = 0
      sub.points = 0
      sub.code = file(fname, "r").read()
      sub.errors = ""
      sub.save()
      
if __name__ == "__main__":
    print sys.argv[1:]
    submit_to_db(sys.argv[1:])

