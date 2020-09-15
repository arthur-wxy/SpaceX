# -*- coding:utf-8 -
import time

from .server_conn import SSHConnect
from .portalRelease import git_pull
from .appRelease import build_vue
from .para_test import zip_dir
from .logger import info


# PORTAL_SERVER1 = ['10.151.66.21', 'crmadmin', 'auxp@ssw0rd']
# PORTAL_SERVER2 = ['10.151.66.23', 'crmadmin', 'auxp@ssw0rd']
# PORTAL_SERVER3 = ['10.151.66.26', 'crmadmin', 'auxp@ssw0rd']
# PORTAL_SERVER4 = ['10.151.66.33', 'crmadmin', 'auxp@ssw0rd']

PATH_INFO = {'portal_front_path': 'D:\Source\Portal-FrontEnd',
             'portal_vue_path': 'D:\Source\Portal-FrontEnd\h5',
             'tmp_path': 'D:\Source\\tmp_files',
             'portal_build_path': 'D:\Source\Portal-FrontEnd\h5\\build',
             'PFrontRelease_path': 'D:\Source\\tmp_files\PFrontRelease.zip',
             'target_path': '/cygdrive/d/workspace/tmp_files/PFrontRelease.zip'
}

# CMD = {'cmd1': 'cd /cygdrive/d/workspace/PortalWebPre && rm -rf static && rm -rf index.html',
#        'cmd2': 'cd /cygdrive/d/workspace/tmp_files && unzip -o PFrontRelease.zip -d /cygdrive/d/workspace/PortalWebPre'
# }


# portal前端的发布,先打包
def build_and_zip():

    # 拉取代码
    git_pull(PATH_INFO['portal_front_path'])
    time.sleep(3)
    # 前端构建
    build_vue(PATH_INFO['portal_vue_path'])
    time.sleep(3)
    # 打包到临时目录
    zip_dir('PFrontRelease', PATH_INFO['portal_build_path'], PATH_INFO['tmp_path'])

# 连接服务器并部署
def conn_and_deploy(host, user, pwd, src, dst, CMD):

    # 连接服务器
    ssh = SSHConnect(hostname=host, username=user, password=pwd)
    ssh.connect()
    ssh.upload(src, dst)
    # 删除D:\workspace\PortalWeb下的static和index,在直接解压
    # if not ssh.exec_cmd(CMD['cmd1']) and ssh.exec_cmd(CMD['cmd2']):
    #     print(info('command execute failed'))
    # else:
    #     print(info('command execute success'))
    ssh.exec_cmd('{}'.format(CMD['cmd1']))
    time.sleep(1)
    ssh.exec_cmd('{}'.format(CMD['cmd2']))
    ssh.disconnect()


if __name__ == '__main__':
    # print(PATH_INFO['portal_front_path'])
    # 前端资源打包
    build_and_zip()
    time.sleep(2)

    # # 测试
    # conn_and_deploy('10.151.66.61', 'crmadmin', 'auxp@ssw0rd', PATH_INFO['PFrontRelease_path'], PATH_INFO['target_path'])
    # print(info('server1(21) deployed'))


    # 部署服务器1
    # conn_and_deploy(PORTAL_SERVER1[0], PORTAL_SERVER1[1], PORTAL_SERVER1[2], PATH_INFO['PFrontRelease_path'], PATH_INFO['target_path'])
    # print(info('server1(21) deployed'))
    # 部署服务器2
    conn_and_deploy(PORTAL_SERVER2[0], PORTAL_SERVER2[1], PORTAL_SERVER2[2], PATH_INFO['PFrontRelease_path'], PATH_INFO['target_path'])
    print(info('server1(23) deployed'))
    # 部署服务器3
    # conn_and_deploy(PORTAL_SERVER3[0], PORTAL_SERVER3[1], PORTAL_SERVER3[2], PATH_INFO['PFrontRelease_path'], PATH_INFO['target_path'])
    # print(info('server1(26) deployed'))
    # 部署服务器4
    # conn_and_deploy(PORTAL_SERVER4[0], PORTAL_SERVER4[1], PORTAL_SERVER4[2], PATH_INFO['PFrontRelease_path'], PATH_INFO['target_path'])
    # print(info('server1(33) deployed, all done!'))
    
    
