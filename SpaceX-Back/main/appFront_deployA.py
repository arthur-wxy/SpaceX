# -*- coding:utf-8 -*-
import time

from server_conn import SSHConnect
from portalRelease import git_pull
from appRelease import build_h5, build_vue
from para_test import zip_dir
from logger import info

#
# APP_SERVER1 = ['10.151.66.17', 'crmadmin', 'auxp@ssw0rd']
# APP_SERVER2 = ['10.151.66.31', 'crmadmin', 'auxp@ssw0rd']

PATH_INFO ={'app_front_path': 'D:\Source\devs\APP-FrontEnd\HtmlSource_app',
            'vue_path': 'D:\Source\devs\APP-FrontEnd\HtmlSource_app\h5-v2',
            'angular_path': 'D:\Source\devs\APP-FrontEnd\HtmlSource_app\h5',
}

CMD = {'cmd1': 'cd /cygdrive/d/workspace/tmp_files && unzip -o appback.zip -d /cygdrive/d/workspace/AppWeb/AppWeb-A-8085/bin',
       'cmd2': 'cd /cygdrive/d/workspace/tmp_files && unzip -o appback.zip -d /cygdrive/d/workspace/AppWeb/AppWeb-A-8086/bin'
}


# portal前端的发布,先打包
def build_and_zip():

    # 拉取代码
    git_pull(PATH_INFO['app_front_path'])
    time.sleep(2)
    # 前端构建
    build_vue(PATH_INFO['vue_path'])
    build_h5(PATH_INFO['angular_path'])
    time.sleep(30)

    # 打包到临时目录
    zip_dir('PFrontRelease', PATH_INFO['portal_build_path'], PATH_INFO['tmp_path'])