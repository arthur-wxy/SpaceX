# -*- coding:utf-8 -*-
import os
import sys
import yaml
import time
import datetime
import logging
import unittest

from main.server_conn import SSHConnect
from main.para_test import zip_dir
from main.appBackEndRelease import compile_sln
from main.appBackUpload import copy_dll
from main.logger import info

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='D:\source\SpaceX\SpaceX-Back\main\log\\release.log',
                    filemode='a')


# 拉取代码
def code_pull(repo_path, branch):
    """
    :param repo_path: 项目的本地仓库路径
    :param branch: 要拉取的分支
    :return:
    """
    os.chdir(repo_path)
    os.system('git pull')
    b = branch.replace(' ', '')  # 如果输入的分支含有空格，去除
    if os.system('git clean -n') == 0:  # 避免因冲突产生无法创建分支的情况，先clean没跟踪的文件
        os.system('git clean -f')
    os.system('git checkout -b {} origin/{} '.format(b, b))  # 每次从远程创建最新分支
    print(datetime.datetime.now().strftime('[%Y-%m-%d %H:%M:%S]') + '======== branch created')
    logging.info('branch created')
    os.system('git pull')  # 创建完拉取一下最新分支


def front_build(src, src_path):
    """
    前端资源的构建
    :param src: vue:0 angular:1
    :param src_path: 构建资源的路径
    :return:
    """
    os.chdir(src_path)
    if src == 0:
        try:
            os.system('npm run build')
            print(info('build completed'))
            # logging.info('build completed')
        except:
            # logging.info('build failed')
            print(info('build failed'))
    else:
        try:
            os.system('start gulp')
        except:
            print(info('gulp failed'))
            # logging.info('gulp failed')


def connect_and_unzip(server_list, src_path, dst_path, cmd):
    """
    连接服务器，传输zip，解压zip
    :param server_list: 要发布的服务器列表
    :param src_path: 要发布的zip本地路径
    :param dst_path: 发布目标路径
    :param cmd: 解压命令
    :return:
    """
    for i in server_list:
        try:
            s = SSHConnect(hostname=i)
            s.connect()
            s.upload(src_path, dst_path)
            s.exec_cmd(cmd)
            s.disconnect()
        except Exception as e:
            # print(e)
            return {'stateCode': '202', 'Msg': 'failed,{}'.format(e)}
    return {'stateCode': '200', 'Msg': 'success'}


def portal_back_release(server_list, branch, dll_list):
    """

    :param server_list: 要发布的服务器列表
    :param branch: 要发布的分支
    :param dll_list: 要发布的dll列表
    :return:
    """
    # 先读一下配置文件，获取路径dll等,以后变量名不要用字母
    with open('../config/config.yaml', 'r', encoding='UTF-8') as f:
        a = yaml.load(f.read(), Loader=yaml.FullLoader)
        repo_path = a['path']['portal_back_path']
        sln_path = a['path']['portal_sln_path']
        dll_path = a['path']['portal_dll_path']
        portal_tmp_path = a['path']['portal_dll_tmp_path']
        tmp_files_path = a['path']['tmp_files_path']
        src_path = a['path']['portal_back_src_path']
        dst_path = a['path']['portal_back_dst_path']
        cmd = a['cmd']['cmd1']

    # 拉取代码
    code_pull(repo_path, branch)
    time.sleep(1)
    # 后端编译
    compile_sln(sln_path)
    time.sleep(1)
    # 复制到临时目录
    copy_dll(dll_path, portal_tmp_path, dll_list)
    #  将此dll目录打包
    zip_dir('PBackRelease', portal_tmp_path, tmp_files_path)
    # 连接服务器，传输zip包并解压到对应目录
    connect_and_unzip(server_list, src_path, dst_path, cmd)


def portal_front_release(server_list, branch, file_list):
    """

    :param server_list: 要发布的服务器列表
    :param branch: 要发布的服务器
    :return:
    """
    pass
    with open('../config/config.yaml', 'r', encoding='UTF-8') as f:
        a = yaml.load(f.read(), Loader=yaml.FullLoader)
        repo_path = a['path']['portal_front_path']
        portal_vue_path = a['path']['portal_vue_path']
        portal_vue_build_path = a['path']['portal_vue_build_path']
        tmp_files_path = a['path']['tmp_files_path']
        src_path = a['path']['portal_front_src_path']
        dst_path = a['path']['portal_front_dst_path']
        cmd = a['path']['cmd3']
    try:
        # 拉取代码
        code_pull(repo_path, branch)
        time.sleep(1)
        # 前端构建
        front_build(0, portal_vue_path)
        time.sleep(1)
        # 直接打包到tmp目录
        zip_dir('pfront', portal_vue_build_path, tmp_files_path)
        # 连接服务器，传输zip，解压
        connect_and_unzip(server_list, src_path, dst_path, cmd)
        return {'stateCode': '200', 'Msg': 'success'}
    except Exception as e:
        return {'stateCode': '202', 'Msg': 'failed,{}'.format(e)}


def app_back_release(server_list, branch, dll_list):
    """

    :param server_list: app的服务器列表
    :param branch: app的分支
    :param dll_list: 要发布的dll
    :return:
    """
    with open('../config/config.yaml', 'r', encoding='UTF-8') as f:
        a = yaml.load(f.read(), Loader=yaml.FullLoader)
        repo_path = a['path']['app_back_path']
        sln_path = a['path']['app_sln_path']
        dll_path = a['path']['app_dll_path']
        app_tmp_path = a['path']['app_tmp_path']
        tmp_files_path = a['path']['tmp_files_path']
        src_path = a['path']['app_back_src_path']
        dst_path = a['path']['app_back_dst_path']
        cmd = a['cmd']['cmd2']
    try:
        # 拉取代码
        code_pull(repo_path, branch)
        time.sleep(1)
        # 编译解决方案
        compile_sln(sln_path)
        time.sleep(1)
        # 拷贝到临时目录
        copy_dll(dll_path, app_tmp_path, dll_list)
        # 打包
        zip_dir('ABackRelease', app_tmp_path, tmp_files_path)
        # 连接服务器并传输zip、解压到对应目录
        connect_and_unzip(server_list, src_path, dst_path, cmd)
        return {'stateCode': '200', 'Msg': 'success'}
    except Exception as e:
        return {'stateCode': '202', 'Msg': 'failed,{}'.format(e)}


def app_front_release(server_list, branch, file_List):
    """
    app的前端发布
    :param server_list:
    :param branch:
    :param file_List:
    :return:
    """
    # 读取一下配置文件
    with open('../config/config.yaml', 'r', encoding='UTF-8') as f:
        a = yaml.load(f.read(), Loader=yaml.FullLoader)
        repo_path = a['path']['app_front_path']
        app_vue_path = a['path']['app_vue_path']
        app_angular_Path = a['path']['app_angular_path']
        app_vue_build_path = a['path']['app_vue_build_path']
        app_angular_build_Path = a['path']['app_angular_build_Path']
        tmp_files_path = a['path']['tmp_files_path']
        app_vue_src_path = a['path']['app_vue_src_path']
        app_vue_dst_path = a['path']['app_vue_dst_path']
        app_angular_src_path = a['path']['app_angular_src_path']
        app_angular_dst_path = a['path']['app_angular_dst_path']
        cmd_4_vue = a['cmd']['cmd4']
        cmd_4_angular = a['cmd']['cmd5']
    try:
        # 拉取代码、前端构建
        code_pull(repo_path, branch)
        time.sleep(1)
        if 'angular' not in file_List:
            front_build(0, app_vue_path)

        else:
            front_build(0, app_vue_path)
            front_build(1, app_angular_Path)
            time.sleep(1)
        # 将前端文件打包到tmp下
        zip_dir('vue', app_vue_build_path, tmp_files_path)
        zip_dir('angular', app_angular_build_Path, tmp_files_path)
        # 连接服务器，传输zip，解压
        for i in server_list:
            s = SSHConnect(hostname=i)
            s.connect()
            s.upload(app_vue_src_path, app_vue_dst_path)
            s.upload(app_angular_src_path, app_angular_dst_path)
            s.exec_cmd(cmd_4_vue)
            s.exec_cmd(cmd_4_angular)
            s.disconnect()
        return {'stateCode': '200', 'Msg': 'success'}
    except Exception as e:
        return {'stateCode': '202', 'Msg': 'failed,{}'.format(e)}


def download_and_unzip(src_path, target_path):
    pass


# 测试
class TestCase(unittest.TestCase):

    def test_app_front(self):
        self.assertEqual(app_front_release(0, 0, ['vue']), 1)
        self.assertEqual(app_front_release(0, 0, ['vue', 'angular']), 2)


if __name__ == '__main__':
    unittest.main()
    # server_list = ['10.151.66.60']
    # branch = '200929feature-TEST'
    # dll_list = ['RekTec.XStudio.Crm.WebApi.dll',
    #             'RekTec.XStudio.Exam.WebApi.dll'
    #             ]
    # # portal 后端发布
    # portal_back_release(server_list, branch, dll_list)
    # # app 后端发布
    # app_back_release(server_list, branch, dll_list)
