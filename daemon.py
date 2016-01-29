import apscheduler
import time
import sys
import json
import toolz
import subprocess
from glob import glob
import os
from os.path import basename, splitext, abspath, join
from apscheduler.triggers.cron import CronTrigger
from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.schedulers.background import BackgroundScheduler, BlockingScheduler

LOGGING = True
START = time.time()

# DECISION: no module loading, but instead having
# a config file for every script run

def main():
    # need to run all files within this directory
    os.chdir(get_parent_dir())

    jobs = dict()

    scheduler = BackgroundScheduler(executors={'default': ThreadPoolExecutor(3)})

    default_config = get_default_config()

    configs = get_config_files()

    for path, config in configs.items():
        id = create_job(config, scheduler)
        jobs[path] = id

    scheduler.start()

    while True:
        time.sleep(5)
        changed = changed_files(jobs)
        added = added_files(jobs)
        for change in changed:
            remove_job(change, scheduler)
            jobs[change] = create_job(changed[change], scheduler)
        for add in added:
            jobs[add] = create_job(added[add], scheduler)


def get_default_config():
    with open('default-config.json', 'r') as f:
        config = json.load(f)
    return config

def get_parent_dir():
    return os.path.dirname(abspath(__file__))

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

def create_job(config, scheduler):
    # dict struct
    interval = config['interval']
    id = str(time.time())
    trigger = CronTrigger(**interval)
    scheduler.add_job(worker, trigger, args=(config,), id=id)
    return id

def worker(config):
    if LOGGING:
        print('Running {}'.format(config['script']))
    call_stack = [config['type'], config['script']]
    for folder in config['watch']:
        subprocess.call(call_stack + [folder, get_parent_dir()])


def remove_job(id, scheduler):
    scheduler.remove_job(id)

def old(file):
    return START < os.path.getmtime(file)

def changed_files(jobs):
    changed = filter(old, jobs)
    new = {c: parse_config(c) for c in changed}
    return toolz.valfilter(exists, new)

def added_files(jobs):
    configs = get_config_files()
    if len(configs) > len(jobs):
        keys = filter(lambda a: a not in jobs, configs)
        return {key: configs[key] for key in keys}
    else:
        return None

def safeify_config():
    pass

if __name__=='__main__':
    main()
