import shutil
import datetime
import functools
import os
from os.path import join

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

def move(files, path):
    if not os.path.exists(path):
        os.makedirs(path)
    for f in files:
        shutil.move(f, path)
