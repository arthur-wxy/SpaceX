#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import shutil
import zipfile
import os
import os.path
import re
import time
import datetime

from logger import info


def time_log(func):
    def wrapper(*args):
        print(info('start packing'))
        func(*args)
        print(info('pack finished'))

    return wrapper


def del_zip(path):
    try:
        os.remove(path)
        print(info('zip deleted'))
    except:
        print(info('zip does not exsit'))


def zip_debug(debug_path):
    """将AppWeb/debug下的文件压缩成zip"""
    # target_zip = 'debug.zip'
    # if target_zip not in os.listdir(debug_path):
    #     target_debug = os.path.join(debug_path, 'debug')
    #     shutil.make_archive(target_debug, 'zip', root_dir=debug_path)
    #     print(info() + '======== pack finished')
    # else:
    #     # print(info() + '======== zip already exsits')
    #     # del_zip(os.path.join(debug_path, 'debug.zip'))
    #     target_debug = os.path.join(debug_path, 'debug')
    #     shutil.make_archive(target_debug, 'zip', root_dir=debug_path)
    #     print(info() + '======== zip regenerated')
    target_debug = os.path.join(debug_path, 'debug')
    shutil.make_archive(target_debug, 'zip', root_dir=debug_path)
    print(info('zip generated'))
    
    
def rename_zip(curDir):
    
    lists = os.listdir(curDir)
    # 列出目录的下所有文件和文件夹保存到lists
    lists.sort(key=lambda fn: os.path.getmtime(curDir + "\\" + fn))  # 按时间排序
    file_new = lists[-1]  # 获取最新的文件保存到file_new
    # 分割文件名与后缀，并保存成list
    oldname = file_new.split('.')
    # 取出文件名部分
    a = oldname[0]
    # 截取下划线之间的字符作为新文件名
    b = a.split('_', 2)[1]
    # 
    for parent, dirnames, filenames in os.walk(curDir):
        for filename in filenames:
            if filename.find(a) != -1:
                newName = filename.replace(a, b)
                print("rename origin" + filename + "to new: " + newName)
                os.rename(os.path.join(parent, filename), os.path.join(parent, newName))
                

def list_dir(path, list_name):  #传入存储的list
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if os.path.isdir(file_path):
            list_dir(file_path, list_name)
        else:
             list_name.append((file_path,os.path.getctime(file_path)))
 
 
def newestfile(target_list):
    newest_file = target_list[0]
    for i in range(len(target_list)):
        if i < (len(target_list)-1) and newest_file[1] < target_list[i+1][1]:
            newest_file = target_list[i+1]
        else:
            continue
    print('newest file is',newest_file)
    return newest_file


def zip_and_move():
    portal_path = r'D:\workspace\PortalWeb\App_Data\Files\Attachment'
    dst_path = r'D:\dst'
    app_attachments = r'D:\workspace\AppWeb\App_Data\Files\Attachment'
    app_packages = r'D:\workspace\AppWeb\Files\Packages'
    list = []
    list_dir(portal_path, list)
    new_file = newestfile(list)
    shutil.copy(new_file[0], dst_path)
    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '======== copy zip to dst')  # 将压缩包复制到dst，以便后续重命名再复制到packages下    
    shutil.copy(new_file[0], app_attachments)     
    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '======== copy zip to attachment')  # 直接将压缩包复制到appdata/files/attachments下
    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '======== renaming')
    rename_zip("D:\dst")
    time.sleep(3)
    list1 = []
    list_dir(dst_path, list1)
    new_file1 = newestfile(list1)
    shutil.copy(new_file1[0], app_packages)
    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '======== copy zip to packages')  # 将重命名后的压缩包复制到app/packages下
    time.sleep(1)
    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '======== release is processing')


if __name__ == '__main__':
    pass
    # zip_debug()
    # zip_and_move()