# -*- coding:utf-8 -*-
import os
import sys
import time
import datetime

from appBackUpload import copy_dll
from appFrontUpload import git_pull
from appBackEndRelease import compile_sln
from dll_module import portal

        
def main():
    git_pull('D:\Source\Portal-BackEnd')
    time.sleep(3)
    compile_sln('D:\Source\Portal-BackEnd\dotnet_xrm\ServiceOne-Portal.sln')
    time.sleep(3)
    copy_dll('D:\Source\Portal-BackEnd\dotnet_xrm\\bin', 'D:\workspace\PortalWeb\\bin', portal())
    time.sleep(3)
    # git_push()



if __name__ == '__main__':
    main()