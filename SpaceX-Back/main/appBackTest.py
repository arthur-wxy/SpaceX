# -*- coding:utf-8 -*-
import os
import sys
import time
import datetime

from appBackUpload import copy_dll
from appFrontUpload import git_pull
from appBackEndRelease import compile_sln
from dll_module import mobile

        
def main():
    git_pull('D:\Source\APP-BackEnd')  # 拉取代码，更新
    time.sleep(3)
    compile_sln('D:\Source\APP-BackEnd\DotNetSource\RekTec.Xmobile.sln')  # 后端编译
    time.sleep(3)
    copy_dll('D:\Source\APP-BackEnd\DotNetSource\\bin', 'D:\workspace\AppWeb\\bin', mobile())  # 复制到workspace
    time.sleep(3)
    # git_push()



if __name__ == '__main__':
    main()