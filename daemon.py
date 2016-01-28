import apscheduler
import time
import sys
import json
import toolz
from glob import glob
import os
from os.path import basename, splitext, abspath, join
from apscheduler.triggers.cron import CronTrigger
from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.schedulers.background import BackgroundScheduler, BlockingScheduler

# DECISION: no module loading, but instead having
# a config file for every script run


def main():
    # need to run all files within this directory
    os.chdir(os.path.dirname(abspath(__file__)))

    scheduler = BlockingScheduler(executors={'default': ThreadPoolExecutor(3)})

    configs = get_config_files()



    for pypath in python_jobs:
        base = splitext(basename(pypath))[0]
        module = imp.load_source(base, pypath)
        _id = create_job(module, scheduler)
        job_id[_id] = module
    scheduler.start()

def get_config_files():
    '''Find all config files and place into
    a loaded dictionary'''
    files = glob(join('jobs', '*config.json'))
    # check if script exists
    configs = {f: parse_config(f) for f in files}
    configs = toolz.valfilter(exists, configs)
    return configs

def parse_config(file_path):
    '''Load config file'''
    with open(file_path, 'r') as f:
        config = json.load(f)
    return config

def exists(d):
    script_path = d.get('script', None)
    return script_path and os.path.exists(script_path)

def create_job(py_mod, scheduler):
    # dict struct
    interval = py_mod.INTERVAL
    watchedFolder = py_mod.WATCHED_FOLDER
    uniqueId = str(time.time())
    trigger = CronTrigger(**interval)
    def closure_job():
        py_mod.main(watchedFolder)
    scheduler.add_job(closure_job, trigger, id=uniqueId)
    return uniqueId

def remove_job(id, scheduler):
    pass

def restart_job():
    pass

def setup():
    pass

def changed_files():
    pass



if __name__=='__main__':
    main()
