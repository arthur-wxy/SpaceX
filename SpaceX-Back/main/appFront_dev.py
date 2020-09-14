# -*- coding:utf-8 -*-
import os
import time
import threading

from server_conn import SSHConnect
from portalRelease import git_pull
from appRelease import build_h5, build_vue
from para_test import zip_dir
from logger import info


def main():
    app_front_path = 'D:\Source\devs\APP-FrontEnd\HtmlSource_app'
    vue_path = 'D:\Source\devs\APP-FrontEnd\HtmlSource_app\h5-v2'
    angular_path = 'D:\Source\devs\APP-FrontEnd\HtmlSource_app\h5'
    vue_zip_path = 'D:\Source\devs\APP-FrontEnd\HtmlSource_app\h5-v2\dist'
    angular_zip_path = 'D:\Source\devs\APP-FrontEnd\HtmlSource_app\h5\\build\debug'
    tmp_path = 'D:\Source\\tmp_files'  # 用来暂存所有压缩包的目录
    target_dir = '/cygdrive/d/workspace/tmp_files/'
    vue_deploy_path = os.path.join(tmp_path, 'vue.zip')
    angular_deploy_path = os.path.join(tmp_path, 'angular.zip')
    vue_target_path = os.path.join(target_dir, 'vue.zip')
    angular_target_path = os.path.join(target_dir, 'angular.zip')
    cmd1 = 'cd /cygdrive/d/workspace/AppWeb/debug && rm -rf v2'
    cmd2 = 'cd /cygdrive/d/workspace/AppWeb/debug && mkdir v2 && cd /cygdrive/d/workspace/tmp_files/ && unzip -d /cygdrive/d/workspace/AppWeb/debug/v2 vue.zip'
    cmd3 = 'cd /cygdrive/d/workspace/tmp_files/ && unzip -o angular.zip -d /cygdrive/d/workspace/AppWeb/debug'
    # git拉取代码,传入app前端仓库路径
    git_pull(app_front_path)
    time.sleep(3)
    # 前端项目构建
    build_vue(vue_path)

    build_h5(angular_path)
    # print(info('gulp done?'))
    # t1 = threading.Thread(target=build_vue, args=(vue_path,))
    # t2 = threading.Thread(target=build_h5, args=(angular_path,))
    # t1.start()
    # time.sleep(2)
    # t2.start()
    time.sleep(30)  # angular构建需等待40s
    # 将构建好的项目压缩

def git():
    git_pull('D:\Source\devs\APP-FrontEnd\HtmlSource_app')

def vue():
    build_vue('D:\Source\devs\APP-FrontEnd\HtmlSource_app\h5-v2')

def h5():
    build_h5('D:\Source\devs\APP-FrontEnd\HtmlSource_app\h5')


def zip():
    vue_zip_path = 'D:\Source\devs\APP-FrontEnd\HtmlSource_app\h5-v2\dist'
    angular_zip_path = 'D:\Source\devs\APP-FrontEnd\HtmlSource_app\h5\\build\debug'
    tmp_path = 'D:\Source\\tmp_files'

    zip_dir('vue', vue_zip_path, tmp_path)
    zip_dir('angular', angular_zip_path, tmp_path)



# 实例化
def conn():
    app_front_path = 'D:\Source\devs\APP-FrontEnd\HtmlSource_app'
    vue_path = 'D:\Source\devs\APP-FrontEnd\HtmlSource_app\h5-v2'
    angular_path = 'D:\Source\devs\APP-FrontEnd\HtmlSource_app\h5'
    vue_zip_path = 'D:\Source\devs\APP-FrontEnd\HtmlSource_app\h5-v2\dist'
    angular_zip_path = 'D:\Source\devs\APP-FrontEnd\HtmlSource_app\h5\\build\debug'
    tmp_path = 'D:\Source\\tmp_files'  # 用来暂存所有压缩包的目录
    target_dir = '/cygdrive/d/workspace/tmp_files/'
    vue_deploy_path = os.path.join(tmp_path, 'vue.zip')
    angular_deploy_path = os.path.join(tmp_path, 'angular.zip')
    vue_target_path = os.path.join(target_dir, 'vue.zip')
    angular_target_path = os.path.join(target_dir, 'angular.zip')
    cmd1 = 'cd /cygdrive/d/workspace/AppWeb/debug && rm -rf v2'
    cmd2 = 'cd /cygdrive/d/workspace/AppWeb/debug && mkdir v2 && cd /cygdrive/d/workspace/tmp_files/ && unzip -d /cygdrive/d/workspace/AppWeb/debug/v2 vue.zip'
    cmd3 = 'cd /cygdrive/d/workspace/tmp_files/ && unzip -o angular.zip -d /cygdrive/d/workspace/AppWeb/debug'
    ssh = SSHConnect(hostname='10.151.66.61')
    # 连接服务器,先将压缩包传输到tmp-files目录下
    ssh.connect()
    ssh.upload(vue_deploy_path, vue_target_path)
    ssh.upload(angular_deploy_path, angular_target_path)
    try:
        # 执行命令行，先删除v2下的vue项目
        ssh.exec_cmd(cmd1)
        # 创建v2目录并将vue.zip解压到此目录
        ssh.exec_cmd(cmd2)
        # angular项目直接解压此目录
        ssh.exec_cmd(cmd3)
        print(info('command execute success'))
    except:
        print(info('command execute failed'))
    # 发布完毕，关闭服务器连接
    ssh.disconnect()

def run():
    vue_path = 'D:\Source\devs\APP-FrontEnd\HtmlSource_app\h5-v2'
    angular_path = 'D:\Source\devs\APP-FrontEnd\HtmlSource_app\h5'
    t1 = threading.Thread(target=build_vue, args=(vue_path,))
    t2 = threading.Thread(target=build_h5, args=(angular_path,))

    t1.start()
    time.sleep(2)
    t2.start()


if __name__ == '__main__':
    # main()
    # zip()
    # conn()
    # build_h5()
    # git()
    # time.sleep(3)
    # vue()
    # time.sleep(3)
    print(info('jack'))
    h5()
    # time.sleep(30)
    # zip()
    # conn()