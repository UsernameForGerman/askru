import os

from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '36se8)23iv7a-ic!1r76&(b1(k*ncd4h3t$2a*+c+j$k#lnvef'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True if os.environ.get('DEBUG', 'True') else False

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '*').split(' ')

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
STATIC_ROOT = os.path.join(BASE_DIR, 'static')


