# -*- coding:utf-8 -*-
import os
import sys
import time
import datetime
import shutil

from .appFrontUpload import git_push
from .portalRelease import git_pull
from .appBackEndRelease import compile_sln
from .dll_module import mobile


def move(source_path, target_path, files):
    """传入源路径，目的路径，及文件名"""
    src = '{}\\{}'.format(source_path, files)
    # print(src)
    dst = '{}\\{}'.format(target_path, files)
    # print(dst)
    shutil.copyfile(src, dst)


def copy_dll(src, dst, dll):
    """
    src源文件路径
    dst目标路径
    dll类型
    """
    # global dll_list

    for i in dll:
        move(src, dst, i)  # 直接调用move
    print(datetime.datetime.now().strftime('[%Y-%m-%d %H:%M:%S]') + '====== Copy Finished!')


def main():
    """
    拉取代码，编译复制，上传git
    """
    git_pull('D:\Source\APP-BackEnd')  # 拉取代码，更新
    time.sleep(3)
    compile_sln('D:\Source\APP-BackEnd\DotNetSource\RekTec.Xmobile.sln')  # 后端编译
    time.sleep(3)
    copy_dll('D:\Source\APP-BackEnd\DotNetSource\\bin', 'D:\Source\workspace\workspace\APP-Back', mobile())  # 复制到workspace
    time.sleep(3)
    git_push()  # 上传git



if __name__ == '__main__':
    main()
    # copy_dll('D:\Source\APP-BackEnd\DotNetSource\\bin', 'D:\Source\workspace\workspace\APP-Back', mobile())