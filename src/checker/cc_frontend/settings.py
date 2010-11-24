import os
import ConfigParser

config = ConfigParser.ConfigParser()
config.read('/usr/local/etc/checker/settings.conf')

#Django Specific config
TIME_ZONE = config.get('django', 'TIME_ZONE')
SITE_ID = 1
TEMPLATE_LOADERS = ( 
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
 )

MIDDLEWARE_CLASSES = ( 
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
)

DATABASE_ENGINE = config.get('database','DATABASE_ENGINE')   
DATABASE_NAME = config.get('database', 'DATABASE_NAME')
DATABASE_USER = config.get('database', 'DATABASE_USER')   
DATABASE_PASSWORD = config.get('database', 'DATABASE_PASSWORD')

ROOT_URLCONF = 'checker.cc_frontend.urls'
TEMPLATE_DIRS = ( 
    os.path.join( os.getcwd(), 'templates/')
 )
MEDIA_URL = config.get('django', 'MEDIA_URL')
ADMIN_MEDIA_PREFIX = config.get('django', 'ADMIN_MEDIA_PREFIX')

INSTALLED_APPS = ( 
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'cc_frontend.web'
 )

# codechecker based custom config
BASE_URL = config.get('apache', 'BASE_URL')
SERVERNAME = config.get('apache', 'SERVERNAME')

# Debug
DEBUG = True
TEMPLATE_DEBUG = DEBUG
