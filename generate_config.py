import json
import os

def main():
    savefile = input('script name: ')

    params = {}
    params['watch'] = ['path1']
    params['interval'] = {
        'year': '*',
        'month': '*',
        'day': '*',
        'hour': '*',
        'minute': '*/1',
        'second': '*'
    }
    params['is_backup'] = True
    params['output'] = False
    params['script'] = 'jobs/' + savefile + '.py'

    if not savefile:
        savefile = 'autoconfig'

    if os.path.exists('jobs'):
        savefile = os.path.join('jobs', savefile)

    with open(savefile + '-config.json', 'w') as f:
        json.dump(params, f, indent=2)

if __name__ == '__main__':
    main()
