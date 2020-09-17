# -*- coding:utf-8 -*-
import os
import time
import yaml

from main.server_conn import SSHConnect
#
# with open('../config/config.yaml', 'r', encoding='UTF-8') as f:
#     a = yaml.load(f.read(), Loader=yaml.FullLoader)
#     print(a['cmd']['cmd1'])
#     print(type(a['cmd']['cmd1']))


def test():
    time.sleep(3)
    s = SSHConnect(hostname='10.151.66.60')
    return 'test success'
