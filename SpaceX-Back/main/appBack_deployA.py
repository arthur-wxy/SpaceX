# -*- coding:utf-8 -*-
import time

from server_conn import SSHConnect
from portalRelease import git_pull
from para_test import zip_dir
from logger import info
from appBackEndRelease import compile_sln
from dll_module import mobile
from appBackUpload import copy_dll
from portalFront_deploy import conn_and_deploy



# APP_SERVER1 = ['10.151.66.17', 'crmadmin', 'auxp@ssw0rd']
# APP_SERVER2 = ['10.151.66.31', 'crmadmin', 'auxp@ssw0rd']
# APP_SERVER3 = ['10.151.66.86', 'crmadmin', 'auxp@ssw0rd']
# APP_SERVER4 = ['10.151.66.87', 'crmadmin', 'auxp@ssw0rd']

PATH_INFO ={'app_back_path': 'D:\Source\APP-BackEnd',
            'sln_path': 'D:\Source\APP-BackEnd\DotNetSource\RekTec.Xmobile.sln',
            'back_dll_path': 'D:\Source\APP-BackEnd\DotNetSource\\bin',
            'ABackRelease_path': 'D:\Source\\tmp_files\mobile_dll',
            'tmp_path': 'D:\Source\\tmp_files',
            'target_path': '/cygdrive/d/workspace/tmp_files/ABackRelease.zip',
            'ABZip_path': 'D:\Source\\tmp_files\\ABackRelease.zip'
}

CMD = {'cmd3': 'unzip -o /cygdrive/d/workspace/tmp_files/ABackRelease.zip -d /cygdrive/d/workspace/AppWeb-B-8085/bin >> log.txt',
       'cmd1': 'cd /cygdrive/d/workspace/tmp_files && unzip -o ABackRelease.zip -d /cygdrive/d/workspace/AppWeb-A-8090/bin >> log.txt',
       'cmd2': 'echo hello'
}


def complie_and_zip():

    # 拉取代码
    git_pull(PATH_INFO['app_back_path'])
    time.sleep(3)
    # 后端编译
    compile_sln(PATH_INFO['sln_path'])
    time.sleep(3)
    # 复制到临时dll目录下
    print(PATH_INFO['back_dll_path'])
    copy_dll(PATH_INFO['back_dll_path'],PATH_INFO['ABackRelease_path'],mobile())
    time.sleep(2)
    a = PATH_INFO['ABackRelease_path']
    b = PATH_INFO['tmp_path']
    # 将此dll目录打包
    zip_dir('ABackRelease', PATH_INFO['ABackRelease_path'], PATH_INFO['tmp_path'])


def exc(host, user, pwd):
    ssh = SSHConnect(hostname=host, username=user, password=pwd)
    ssh.connect()
    # print(CMD['cmd3'])
    # ssh.exec_cmd('{}'.format(CMD['cmd1']))
    print(ssh.exec_cmd('{}'.format(CMD['cmd1'])))
    # ssh.exec_cmd('{}'.format(CMD['cmd1']))
    
    ssh.disconnect()

if __name__ == '__main__':
    
#     D:\workspace\AppWeb-A-8089\bin
#     D:\workspace\AppWeb-A-8090\bin 
# 或
#     D:\workspace\AppWeb-B-8085\bin
#     D:\workspace\AppWeb-B-8086\bin

    # 后端编译打包
    complie_and_zip()
    time.sleep(2)
    # # # 部署服务器1
    conn_and_deploy(APP_SERVER1[0], APP_SERVER1[1], APP_SERVER1[2],PATH_INFO['ABZip_path'], PATH_INFO['target_path'])
    exc(APP_SERVER1[0], APP_SERVER1[1], APP_SERVER1[2])
    print(info('server1(17) deployed'))

    conn_and_deploy(APP_SERVER2[0], APP_SERVER2[1], APP_SERVER2[2],PATH_INFO['ABZip_path'], PATH_INFO['target_path'])
    exc(APP_SERVER2[0], APP_SERVER2[1], APP_SERVER2[2])
    print(info('server1(31) deployed'))

    conn_and_deploy(APP_SERVER3[0], APP_SERVER3[1], APP_SERVER3[2],PATH_INFO['ABZip_path'], PATH_INFO['target_path'])
    exc(APP_SERVER3[0], APP_SERVER3[1], APP_SERVER3[2])
    print(info('server1(86) deployed'))

    conn_and_deploy(APP_SERVER4[0], APP_SERVER4[1], APP_SERVER4[2],PATH_INFO['ABZip_path'], PATH_INFO['target_path'])
    exc(APP_SERVER4[0], APP_SERVER4[1], APP_SERVER4[2])
    print(info('server1(87) deployed'))
    # # 部署服务器2
    # conn_and_deploy(APP_SERVER2[0], APP_SERVER2[1], APP_SERVER2[2],PATH_INFO['ABZip_path'], PATH_INFO['target_path'])
    # print(info('server1(31) deployed'))
    # print(CMD['cmd1'])