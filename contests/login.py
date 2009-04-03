from django.conf import settings
from django.contrib.auth.models import User, check_password
from django.contrib.auth import authenticate, login

from MySQLdb import *
from md5 import *
