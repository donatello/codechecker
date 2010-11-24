import os
import sys
import shutil
from distutils.core import setup
from django.core.management import execute_manager


# TODO:One step installation file

prefix = "/usr/local/"
backend_conf = prefix + 'etc/checker/'
frontend_conf = prefix + 'etc/apache/'
media_dir = prefix + 'share/checker/' 

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

# create media directory
if not os.path.exists( media_dir ) :
    os.mkdir( media_dir )

#copy the codechecker.conf to @prefix/etc/checker
shutil.copy( os.path.join( os.getcwd(), 'conf/codechecker.conf'), 
            os.path.join( backend_conf, 'codechecker.conf' ) )

#copy the apache conf file
shutil.copy( os.path.join( os.getcwd(), 'conf/django.conf'), 
            os.path.join( frontend_conf, 'django.conf') )

#copy the media folder to /usr/share/checker/media
# and remove it if already present 
if os.path.exists( media_dir + 'media/'):
    shutil.rmtree( media_dir + 'media/' )

if os.path.exists( '/var/www/media/' ):
    shutil.rmtree('/var/www/media/')
    exit(1)

shutil.copytree(os.getcwd() + '/media', 
                media_dir + 'media/' )

#this is a temporary copy to /www/media
shutil.copytree(os.getcwd() + '/media', 
                '/var/www/media/' )

# Now to run syncdb - settings should already be in place
# It would not have come to this level else
# currently running manage.py syndb, how to call it here ?

# TODO: call manage.py syncdb from here 
# TODO: add django.conf to apache's include directory
# TODO: copy media to /usr/share/checker/media - DOcRoot has already added
# TODO: Default populate
# TODO: Run a Unit test 
# TODO: Run setuid generation - secexec.o 
