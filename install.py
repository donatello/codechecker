import os
import sys
import shutil
from distutils.core import setup
from django.core.management import execute_manager


# TODO:One step installation file

prefix = "/usr/local/"
backend_conf = prefix + 'etc/checker/'
frontend_conf = prefix + 'etc/apache/' 

#check if django exists first
try :
    import django
except ImportError :
    sys.stderr.write( ''' 
---------------------------------------------------------------------------
Could not find Django, please install Django first.\n
sys.stderr.write( "Please install Django from www.djagoproject.com.\n
---------------------------------------------------------------------------
''' )
    exit(1)
# check if python mysql exists
try :
    import MySQLdb
except ImportError :
    sys.stderr.write( '''
---------------------------------------------------------------------------
python-mysqldb is not installed. Please install from apt/yum\n
---------------------------------------------------------------------------
''' )
    exit(1)
    
#Copy the settings.py from sample file and ask to populate the mysql data
shutil.copy( os.path.join( os.getcwd(), 'conf/settings.conf' ),
             os.path.join( backend_conf, 'settings.conf' ) )

# copy all python modules
ret_code = os.system( "python setup.py install" )
if not ret_code == 0 :
    sys.exit(ret_code)


# create etc/checker conf directory if not exists already 
if not os.path.exists( backend_conf ):
    os.mkdir( backend_conf )

# create etc/apache conf directory if not exists already     
if not os.path.exists( frontend_conf ):
    os.mkdir( frontend_conf )

#copy the codechecker.conf to @prefix/etc/checker
shutil.copy( os.path.join( os.getcwd(), 'conf/codechecker.conf'), 
            os.path.join( backend_conf, 'codechecker.conf' ) )

#copy the apache conf file
shutil.copy( os.path.join( os.getcwd(), 'conf/django.conf'), 
            os.path.join( frontend_conf, 'django.conf') )


# Now to run syncdb - settings should already be in place
# It would not have come to this level else
# currently running manage.py syndb, how to call it here ?
# TODO: call manage.py syncdb from here 


