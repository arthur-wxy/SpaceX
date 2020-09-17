# -*- coding:utf-8 -*-
import os
import sys
import yaml
import time
import datetime
import logging


from main.server_conn import SSHConnect
from main.para_test import zip_dir
from main.appBackEndRelease import compile_sln
from main.appBackUpload import copy_dll
from main.appFrontUpload import build_h5 as run_gulp
from main.appFrontUpload import build_vue


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
        portal_back_src_path = a['path']['portal_back_src_path']
        portal_back_dst_path = a['path']['portal_back_dst_path']
        unzip_portal_cmd = a['cmd']['cmd1']

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
    # 实例化连接，连接服务器，传输zip包并解压到对应目录
    for i in server_list:
        try:
            s = SSHConnect(hostname=i)
            s.connect()
            s.upload(portal_back_src_path, portal_back_dst_path)
            s.exec_cmd(unzip_portal_cmd)
            s.disconnect()
        except Exception as e:
            print(e)
            # logging.error(e)


def portal_front_release(server_list, branch, dll_list):
    """

    :param server_list: 要发布的服务器列表
    :param branch: 要发布的服务器
    :param dll_list:
    :return:
    """
    pass


def app_back_release(server_list, branch, dll_list):
    """

    :param server_list: app的服务器列表
    :param branch: app的分支
    :param dll_list: 要发布的dll
    :return:
    """
    with open('../config/config.yaml', 'r', encoding='UTF-8') as f:
        a = yaml.load(f.read(), Loader=yaml.FullLoader)
        repo_path = a['path']['']

    # 拉取代码
    code_pull(repo_path, branch)
    # 编译解决方案
    # 拷贝到临时目录
    # 打包
    # 连接服务器并传输zip、解压到对应目录




if __name__ == '__main__':
    server_list = ['10.151.66.60']
    branch = '200929feature-TEST'
    dll_list = ['RekTec.XStudio.Crm.WebApi.dll',
                'RekTec.XStudio.Exam.WebApi.dll'
                ]
    portal_back_release(server_list, branch, dll_list)
