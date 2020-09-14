import time

from main.logger import info


def just_4_test(msg):
    print('{} just begin'.format(msg))
    time.sleep(3)
    print('done!')