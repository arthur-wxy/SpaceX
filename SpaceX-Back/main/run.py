import os
import time


def run(scripts_name):
    scripts_path = 'D:\pythonscripts'
    os.chdir(scripts_path)
    os.system('python {} origin/200827featrue-TEST'.format(scripts_name))


if __name__ == '__main__':
    run('appFront_dev.py')