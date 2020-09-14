# -*- coding:utf-8 -*-
import time

from server_conn import SSHConnect
from portalRelease import git_pull
from para_test import zip_dir
from appBackEndRelease import compile_sln
from dll_module import portal
from appBackUpload import copy_dll
from logger import info


def main():

    portal_back_path = 'D:\Source\devs\Portal-BackEnd'
    portal_sln_path = 'D:\Source\devs\Portal-BackEnd\dotnet_xrm\ServiceOne-Portal.sln'
    cmd = 'cd /cygdrive/d/workspace/tmp_files && unzip -o pback.zip -d /cygdrive/d/workspace/PortalWeb/bin'

    # 拉取代码
    git_pull(portal_back_path)
    time.sleep(3)
    # 编译解决方案
    compile_sln(portal_sln_path)
    time.sleep(3)
    # 复制到临时dll目录下
    copy_dll('D:\Source\devs\Portal-BackEnd\dotnet_xrm\\bin', 'D:\Source\\tmp_files\portal_dll', portal())
    # 将此dll目录打包
    zip_dir('pback', 'D:\Source\\tmp_files\portal_dll', 'D:\Source\\tmp_files')
    # 实例化连接
    ssh = SSHConnect()
    # 连接服务器，将dll压缩包上传到tmpfiles目录下
    ssh.connect()
    ssh.upload('D:\Source\\tmp_files\\pback.zip', '/cygdrive/d/workspace/tmp_files/pback.zip')
    # 直接解压缩到bin目录下
    if not ssh.exec_cmd(cmd):
        print(info('command execute failed'))
    else:
        print(info('command execute success'))
    # 关闭连接
    ssh.disconnect()


if __name__ == '__main__':
    main()