# -*- coding:utf-8 -*-
import os
import yaml


with open('../config/config.yaml', 'r',encoding='UTF-8') as f:
    a = yaml.load(f.read(), Loader=yaml.FullLoader)
    print(a['cmd']['cmd1'])
    print(type(a['cmd']['cmd1']))