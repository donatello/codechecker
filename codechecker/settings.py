#Django Specific config
TIME_ZONE = 'Asia/Kolkata'
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

#Database connectivity
#### EDIT THIS SECTION WITH YOUR DATABASE DETAILS ####
DATABASE_ENGINE = 'mysql'     
DATABASE_NAME = 'codechecker'
DATABASE_USER = 'checker'   
DATABASE_PASSWORD = 'checker123' 
###########################



# codechecker based django config
ROOT_URLCONF = 'codechecker.root_url'
TEMPLATE_DIRS = ( 
    '/opt/checker/templates',
 )
MEDIA_ROOT = '/opt/checker/media/'
MEDIA_URL = '/media/'
ADMIN_MEDIA_PREFIX = '/media/'
INSTALLED_APPS = ( 
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'codechecker.contests',
 )

# codechecker based custom config
BASE_URL = '/site/'
SERVERNAME = 'checker.example.com'

# Debug
DEBUG = True
TEMPLATE_DEBUG = DEBUG
