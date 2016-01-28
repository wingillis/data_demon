import apscheduler
import time
import imp
import sys
from glob import glob
import os
from os.path import basename, splitext, abspath
from os.path import join
from apscheduler.triggers.cron import CronTrigger
from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.schedulers.background import BackgroundScheduler, BlockingScheduler

# DECISION: no module loading, but instead having
# a config file for every script run


def main():
    os.chdir(os.path.dirname(abspath(__file__)))
    job_id = dict()
    # sys.path.append(abspath('jobs'))
    print(abspath('jobs'))
    python_jobs = glob(join('jobs', '*.py'))
    scheduler = BlockingScheduler(executors={'default': ThreadPoolExecutor(3)})
    for pypath in python_jobs:
        base = splitext(basename(pypath))[0]
        module = imp.load_source(base, pypath)
        _id = create_job(module, scheduler)
        job_id[_id] = module
    scheduler.start()


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
