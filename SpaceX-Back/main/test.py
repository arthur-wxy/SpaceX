import yaml
import os


with open('../config/config.yaml', 'r') as f:
    a = yaml.load(f.read(), Loader=yaml.FullLoader)

    print(type(a))