# -*- coding:utf-8 -*-
import time

from server_conn import SSHConnect
from .portalRelease import git_pull
from para_test import zip_dir
from appBackEndRelease import compile_sln
from dll_module import portal
from appBackUpload import copy_dll
from logger import info
from portalFront_deploy import conn_and_deploy


# PORTAL_SERVER1 = ['10.151.66.21', 'username', 'password']
# PORTAL_SERVER2 = ['10.151.66.23', 'username', 'password']
# PORTAL_SERVER3 = ['10.151.66.26', 'username', 'password']
# PORTAL_SERVER4 = ['10.151.66.33', 'username', 'password']

PORTAL_SERVER2 = ['10.151.66.60', 'crmadmin', 'auxp@ssw0rd']

PATH_INFO ={'portal_back_path': 'D:\Source\Portal-BackEnd',
            'sln_path': 'D:\Source\Portal-BackEnd\dotnet_xrm\ServiceOne-Portal.sln',
            'back_dll_path': 'D:\Source\Portal-BackEnd\dotnet_xrm\\bin',
            'PBackRelease_path': 'D:\Source\\tmp_files\portal_dll',
            'tmp_path': 'D:\Source\\tmp_files',
            'target_path': '/cygdrive/d/workspace/tmp_files/PBackRelease.zip',
            'PBZip_path': 'D:\Source\\tmp_files\\PBackRelease.zip'
}

CMD = {'cmd1': 'cd /cygdrive/d/workspace/tmp_files && unzip -o PBackRelease.zip -d /cygdrive/d/workspace/PortalWebPre/bin',
       'cmd2': 'pwd'
}


def complie_and_zip():

    # 拉取代码
    git_pull(PATH_INFO['portal_back_path'])
    time.sleep(3)
    # 后端编译
    compile_sln(PATH_INFO['sln_path'])
    time.sleep(3)
    # 复制到临时dll目录下
    copy_dll(PATH_INFO['back_dll_path'], PATH_INFO['PBackRelease_path'], portal())
    # 将此dll目录打包
    zip_dir('PBackRelease',PATH_INFO['PBackRelease_path'],PATH_INFO['tmp_path'])


# 测试
def exc():
    ssh = SSHConnect(hostname=PORTAL_SERVER2[0], username=PORTAL_SERVER2[1], password=PORTAL_SERVER2[2])
    ssh.connect()
    # print(CMD['cmd1'])
    # ssh.exec_cmd('{}'.format(CMD['cmd1']))
    # ssh.upload(src, dst)
    ssh.exec_cmd('{}'.format(CMD['cmd1']))
    print(ssh.exec_cmd('{}'.format(CMD['cmd1'])))
    ssh.disconnect()


if __name__ == '__main__':
    # exc()


    # 后端编译打包
    complie_and_zip()
    # time.sleep(2)
    conn_and_deploy(PORTAL_SERVER2[0], PORTAL_SERVER2[1], PORTAL_SERVER2[2], PATH_INFO['PBZip_path'], PATH_INFO['target_path'])
    print(info('server1(60) deployed'))
    # 部署服务器1
    #     conn_and_deploy(PORTAL_SERVER1[0], PORTAL_SERVER1[1], PORTAL_SERVER1[2], PATH_INFO['PBZip_path'], PATH_INFO['target_path'])
    #print(info('server1(21) deployed'))
    # 部署服务器2
    # conn_and_deploy(PORTAL_SERVER2[0], PORTAL_SERVER2[1], PORTAL_SERVER2[2],PATH_INFO['PBZip_path'], PATH_INFO['target_path'])
    # print(info('server1(23) deployed'))
    # 部署服务器3
    # conn_and_deploy(PORTAL_SERVER3[0], PORTAL_SERVER3[1], PORTAL_SERVER3[2], PATH_INFO['PBZip_path'], PATH_INFO['target_path'])
    # print(info('server1(26) deployed'))
    ## 部署服务器4
    #conn_and_deploy(PORTAL_SERVER4[0], PORTAL_SERVER4[1], PORTAL_SERVER4[2], PATH_INFO['PBZip_path'], PATH_INFO['target_path'])
    #print(info('server1(33) deployed, all done!'))

