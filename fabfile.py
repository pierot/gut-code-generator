from fabric.api import *
from fabric.contrib.files import exists, contains, append
from fabric.colors import cyan, blue
from datetime import datetime

###############################################################################
# ALTER THESE 
env.hosts = ['noort.be']
env.user  = 'root'
env.port = 33

DOMAIN = 'gut.noort.be'
PROJECT_NAME = 'code-generator'
PORT = 3001
APP_FILE = 'server'

SITE_ROOT = '/srv/www/%s/public' % DOMAIN

# GNUTAR is needed when deploying to Ubuntu (or other distro?)
TAR = '/usr/bin/gnutar'
###############################################################################

VERSION = datetime.now().strftime('%Y%m%d')
ARCHIVE_NAME = '%s_%s.tar.gz' % (PROJECT_NAME, VERSION)
APP_ROOT = '%s/%s/' % (SITE_ROOT, PROJECT_NAME)

def pack():
  print(cyan("PACKING"))

  # Creating local distribution directory
  local('mkdir -p dist')

  # Creating archive
  local('%s -zcf ./dist/%s $(git ls-files | sed -n "/.DS_Store/!p")' % (TAR, ARCHIVE_NAME), capture=False)

def create_and_clean(dir_name):
  if not exists(dir_name):
    run('mkdir -p %s' % dir_name)
  else:
    run('rm -rf %s*' % dir_name)

def deploy():
  print(cyan("DEPLOY"))

  # Uploading
  put('./dist/%s' % ARCHIVE_NAME, '/tmp/%s' % ARCHIVE_NAME)

  create_and_clean(APP_ROOT)

  with cd('/tmp'):
    create_and_clean('%s/' % PROJECT_NAME)

    # Unarchive
    run('tar -zxf %s -C %s' % (ARCHIVE_NAME, PROJECT_NAME))

    # Move all files to app root
    run('mv %s/* %s' % (PROJECT_NAME, APP_ROOT))

  run('%s/scripts/create-upstart.sh %s %s %s' % (DOMAIN, APP_FILE, PORT))
