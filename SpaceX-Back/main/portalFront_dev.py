# -*- coding:utf-8 -*-
import os
import time

from server_conn import SSHConnect
from portalRelease import git_pull
from appRelease import build_vue
from para_test import zip_dir
from logger import info


def main():

    portal_front_path = 'D:\Source\devs\Portal-FrontEnd'
    portal_vue_path = 'D:\Source\devs\Portal-FrontEnd\h5'
    tmp_path = 'D:\Source\\tmp_files'
    cmd1 = 'cd /cygdrive/d/workspace/PortalWeb && rm -rf static && rm -rf index.html'
    cmd2 = 'cd /cygdrive/d/workspace/tmp_files && unzip -o pfront.zip -d /cygdrive/d/workspace/PortalWeb'

    # 拉取portal前端代码
    git_pull(portal_front_path)
    time.sleep(3)
    # 前端项目构建
    build_vue(portal_vue_path)
    time.sleep(3)
    # 构建完打包到tmpfiles目录下
    zip_dir('pfront','D:\Source\devs\Portal-FrontEnd\h5\\build', tmp_path)
    # 实例化连接
    ssh = SSHConnect()
    # 连接服务器后，先将压缩包传输到tmp-files目录下
    ssh.connect()
    ssh.upload('D:\Source\\tmp_files\pfront.zip', '/cygdrive/d/workspace/tmp_files/pfront.zip')
    # 删除D:\workspace\PortalWeb下的static和index,在直接解压
    if not ssh.exec_cmd(cmd1) and ssh.exec_cmd(cmd2):
        print(info('command execute failed'))
    else:
        print(info('command execute success'))
    ssh.disconnect()


if __name__ == '__main__':
    main()
    # zip_dir('pfront','D:\Source\Portal-FrontEnd\h5\\build', 'D:\Source\\tmp_files')
