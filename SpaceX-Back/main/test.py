
import os
import yaml


with open('../config/config.yaml', 'r') as f:
    a = yaml.load(f.read(), Loader=yaml.FullLoader)
    print(a['dll']['app'])
    print(type(a))