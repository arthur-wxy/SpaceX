# -*- coding:utf-8 -*-
import os
import sys
import time
import datetime


from appFrontUpload import git_push
from portalRelease import git_pull, copy_dir
from appRelease import build_vue


def main():
    git_pull('D:\Source\Portal-FrontEnd')
    time.sleep(3)
    build_vue('D:\Source\Portal-FrontEnd\h5')
    time.sleep(3)
    print(datetime.datetime.now().strftime('[%Y-%m-%d %H:%M:%S]') + '====== please wait...')
    copy_dir('D:\Source\Portal-FrontEnd\h5\\build', 'D:\Source\workspace\workspace\PORTAL-Front')
    time.sleep(3)
    git_push()



if __name__ == '__main__':
    main()