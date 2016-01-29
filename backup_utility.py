import shutil
import datetime
import functools
import os
import time as t
import json
from os.path import join

BACKUP = None

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

def get_config(file):
    if file.endswith('.json'):
        with open(file, 'r') as f:
            return json.load(f)
    else:
        file = os.path.splitext(file)[0] + '-config.json'
        with open(file, 'r') as f:
            return json.load(f)

def set_default(file):
    global BACKUP
    config = get_config(file)
    BACKUP = config.get('backup_location', BACKUP)

def move(files, path):
    path = join(BACKUP, make_path(path))
    if not os.path.exists(path):
        os.makedirs(path)
    for f in files:
        shutil.move(f, path)

BACKUP = get_config('default-config.json')['backup_location']
