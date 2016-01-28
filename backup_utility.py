import shutil
import datetime
import functools
import os
import time as t
from daemon import get_default_config
from os.path import join

DEFAULT = get_default_config()

def date():
    return str(datetime.date.today())

def time():
    return str(datetime.datetime.now())

def project(name):
    return name

def custom(func):
    return func()

def make_path(params):
    return functools.reduce(join, params)

def component(name):
    return name

def old_file(path):
    return t.time() - os.path.getmtime(path) > 2*60

def move(files, path):
    path = join(DEFAULT['backup_location'], make_path(path))
    if not os.path.exists(path):
        os.makedirs(path)
    for f in files:
        shutil.move(f, path)
