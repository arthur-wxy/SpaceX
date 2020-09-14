# -*- coding:utf-8 -*-
import os
import sys
import time
import datetime

from appRelease import build_h5, build_vue, del_file, del_files
from portalRelease import git_pull, copy_dir


def git_push():
    os.chdir('D:\\Source\\workspace\\workspace')  # 进入暂存区目录
    # os.system('git status')
    if os.system('git add .') == 0:
        os.system("git commit -m 'update'")
    else:
        print(datetime.datetime.now().strftime('[%Y-%m-%d %H:%M:%S]') + '====== somethin went wrong')
    os.system('git push')
    time.sleep(3)
    print(datetime.datetime.now().strftime('[%Y-%m-%d %H:%M:%S]') + '====== Upload Finished!')


def main():
    """
    拉取代码，更新代码
    前端打包
    复制到暂存区workspace
    推到git
    """
    git_pull('D:\Source\APP-FrontEnd')
    time.sleep(3)
    build_vue('D:\Source\APP-FrontEnd\HtmlSource_app\h5-v2')
    build_h5('D:\Source\APP-FrontEnd\HtmlSource_app\h5')
    print(datetime.datetime.now().strftime('[%Y-%m-%d %H:%M:%S]') + '====== please wait...')
    time.sleep(30)  # 等待gulp执行完,h5有个controler.js生成时间大约30s，所以等待30s
    del_files('D:\\Source\\workspace\\workspace\\APP-Front\\h5-v2')
    time.sleep(3)
    copy_dir('D:\\Source\\APP-FrontEnd\\HtmlSource_app\\h5-v2\\dist',
            'D:\\Source\\workspace\\workspace\\APP-Front\\h5-v2')  # vue复制到h5-v2
    copy_dir('D:\\Source\\APP-FrontEnd\\HtmlSource_app\\h5\\build\\debug',
            'D:\\Source\\workspace\\workspace\\APP-Front\\h5')  # auglar复制到h5 
    time.sleep(3)
    git_push()
    

if __name__ == '__main__':
    main()
    # del_files('D:\\Source\\workspace\\workspace\\APP-Front\\h5-v2')