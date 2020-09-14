# -*- coding:utf-8 -*-
import os
import shutil


def main(build_path, target_source):
    for files in os.listdir(build_path):
        name = os.path.join(build_path, files)
        back_name = os.path.join(target_source, files)
        if os.path.isfile(name):
            if os.path.isfile(back_name):                
                shutil.copy(name, back_name)
            else:
                shutil.copy(name, back_name)
        else:
            if not os.path.isdir(back_name):
                os.makedirs(back_name)
            main(name, back_name)


if __name__ == '__main__':
    main('C:\\Users\\crmadmin\\Desktop\\dst', 'C:\\Users\\crmadmin\\Desktop\\dst2')
