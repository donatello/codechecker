from django.db import models
from django.contrib.auth.models import User
import datetime

PROBLEM_TYPES = (
    ('Simple','Single Input,Single Output file'),
    ('Multiple','Multiple Input and Output files'),
    ('Complex','Different Point schemes'),
)

LANG_TYPES = (
    ('c','C'),
    ('cpp','C++'),
    #('java','JAVA'),
    #('py','PYTHON'),
    #('pl','PERL'),
)

RESULT_TYPES = (
    ('ACC', 'Accepted'),
    ('PE', 'Presentation Error'),
    ('WA', 'Wrong Answer'),
    ('TLE', 'Time Limit Exceeded'),
    ('MLE', 'Memory Limit Exceeded'),
    ('CMPE', 'Compile Error'),
    ('CMP', 'Compiling' ),
    ('OUTE', 'Output FileSize Exceeded'),
    ('ABRT', 'Abort Called!'),
    ('RUN','Running Test cases'),
    ('SEG', 'Segmentation Fault'),
    ('FRK','Fork Error'),
    ('QU','Queued'),
    ('UNKN', 'Unknown error Occured'),    
    ('FPE', 'Floating Pointing Exception'),
)

# Create your models here.
class Contest(models.Model):
    name = models.CharField(max_length = 25)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_active = models.BooleanField(default=False)
    
    def __unicode__(self):
        return self.name
        
        
class Problem(models.Model):
    ID = models.AutoField(primary_key=True)
    contest = models.ForeignKey(Contest)
    pcode = models.CharField(max_length = 25)
    ptype = models.CharField(max_length=50, choices=PROBLEM_TYPES)
    pstatement = models.TextField()
    input_data= models.TextField()
    output_data= models.TextField()
    tlimit = models.IntegerField()
    mlimit = models.IntegerField()
    is_practisable = models.BooleanField()
    points = models.IntegerField()    
    def __unicode__(self):
        return self.pcode

class Submission(models.Model):
    ID = models.AutoField(primary_key=True)
    user = models.ForeignKey(User)
    problem = models.ForeignKey(Problem)
    time = models.DateTimeField(default=datetime.datetime.now())
    lang = models.CharField(max_length = 5, choices=LANG_TYPES, default='c')
    comments = models.TextField(default='NULL')
    result = models.CharField(max_length = 5, choices=RESULT_TYPES, default='QU')
    code = models.TextField()
            
    def __unicode__(self):
        ret = str(self.ID)
        return ret     

class Ranklist(models.Model):
    ID = models.AutoField(primary_key=True)
    user = models.ForeignKey(User)
    problem = models.ForeignKey(Problem)
    submission = models.ForeignKey(Submission)
    points = models.IntegerField(default=0)
    
    def __unicode__(self):
        ret = str(self.ID)
        return ret
        
class Final(models.Model):
    user = models.ForeignKey(User)
    email = models.EmailField()
    prelims_points = models.IntegerField(default=0)
    finals_points = models.IntegerField(default=0)
    
             
