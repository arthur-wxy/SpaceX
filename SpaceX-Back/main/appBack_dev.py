# -*- coding:utf-8 -*-
import os
import time

from server_conn import SSHConnect
from portalRelease import git_pull
from para_test import zip_dir
from logger import info
from appBackEndRelease import compile_sln
from dll_module import mobile
from appBackUpload import copy_dll

def main():

    app_back_path = 'D:\Source\devs\APP-BackEnd'
    app_sln_path = 'D:\Source\devs\APP-BackEnd\DotNetSource\RekTec.Xmobile.sln'
    cmd = 'cd /cygdrive/d/workspace/tmp_files && unzip -o appback.zip -d /cygdrive/d/workspace/AppWeb/bin'

    # 拉取代码
    git_pull(app_back_path)
    time.sleep(3)
    # 编译解决方案
    compile_sln(app_sln_path)
    time.sleep(3)
    # 将需要发布的dll先复制到临时dll目录
    copy_dll('D:\Source\devs\APP-BackEnd\DotNetSource\\bin', 'D:\Source\\tmp_files\mobile_dll', mobile())
    # 将此dll目录打包
    zip_dir('appback', 'D:\Source\\tmp_files\mobile_dll', 'D:\Source\\tmp_files')
    # 实例化连接
    ssh = SSHConnect()
    # 连接服务器，将dll压缩包上传到tmpfiles目录下
    ssh.connect()
    ssh.upload('D:\Source\\tmp_files\\appback.zip', '/cygdrive/d/workspace/tmp_files/appback.zip')
    # 直接解压缩到bin目录下
    if not ssh.exec_cmd(cmd):
        print(info('command execute failed'))
    else:
        print(info('command execute success'))
    # 关闭连接
    ssh.disconnect()
    

if __name__ == '__main__':
    main()

