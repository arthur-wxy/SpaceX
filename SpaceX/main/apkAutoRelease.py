#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import shutil
import zipfile
import os
import os.path
import re
import time
import datetime

from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains


dst_path = r'C:\Users\crmadmin\Desktop\dst'
portal_path = r'D:\workspace\PortalWeb\App_Data\Files\Attachment'
app_attachments = r'D:\workspace\AppWeb\App_Data\Files\Attachment'
app_packages = r'D:\workspace\AppWeb\Files\Packages'

def zip_files(debug_path):

    """
    将AppWeb/debug下的文件压缩成zip
    将zip复制到指定文件夹下
    """
    target_debug = os.path.join(debug_path, 'debug')
    print(datetime.datetime.now().strftime('[%Y-%m-%d %H:%M:%S]') + '======== 正在打包')
    ret = shutil.make_archive(target_debug, 'zip', root_dir=debug_path)
    print(datetime.datetime.now().strftime('[%Y-%m-%d %H:%M:%S]') + '======== 打包完成')


def create_new_version():
    """
    portal端新建版本号并上传apk包，发布
    """
    driver = webdriver.Chrome()
    driver.get("http://10.151.66.60:8091/admin/#/")
    driver.maximize_window()
    time.sleep(1)
    # 输入账号密码登录
    driver.find_element_by_class_name("el-input__inner").send_keys("admin")
    time.sleep(1)
    driver.find_element_by_xpath("/html/body/div/div/div[2]/form/div[2]/div/div/input").send_keys("P@ssw0rd")
    time.sleep(1)
    driver.find_element_by_xpath("/html/body/div/div/div[2]/form/div[3]/div/div/input").send_keys("AUX")
    time.sleep(1)
    driver.find_element_by_class_name("el-button--primary").click()
    time.sleep(3)
    # 版本
    driver.find_element_by_xpath("/html/body/div[1]/div/div[1]/ul/div[3]/li/ul/li[4]").click()
    time.sleep(3)
    # 新增
    driver.find_element_by_class_name("el-icon-plus").click()
    time.sleep(2)
    # 点击类型
    driver.find_element_by_class_name("el-icon-caret-top").click()
    time.sleep(1)
    # 鼠标悬停选择类型
    mouse = driver.find_element_by_xpath("/html/body/div[3]/div/div[1]/ul/li[1]/span")
    ActionChains(driver).move_to_element(mouse).click().perform()
    time.sleep(1)
    # 输入版本号
    driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div[2]/div/div[5]/div/div/div[2]/form/div[1]\
    /div[2]/div/div/div[1]/input").send_keys("2.14.2.58")
    time.sleep(1)
    # 输入说明
    driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div[2]/div/div[5]/div/div/div[2]/form/div[2]\
    /div/div/div/div/input").send_keys("test_2.14.2.58")
    time.sleep(1)
    # 选择是否必须升级
    driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div[2]/div/div[5]/div/div/div[2]/form/div[3]\
    /div[1]/div/div/div/div[1]/i").click()
    time.sleep(1)
    mouse1 = driver.find_element_by_xpath("/html/body/div[4]/div/div[1]/ul/li[2]/span")
    ActionChains(driver).move_to_element(mouse1).click().perform()
    time.sleep(3)
    # 保存
    driver.find_element_by_class_name("el-icon-upload").click()
    time.sleep(5)
    driver.close()


def api_upload_file():
    pass


def rename_apk(curDir):
    """
    将上传到portalWeb下的最新apk重命名
    """
    lists = os.listdir(curDir) # 列出目录的下所有文件和文件夹保存到lists
    lists.sort(key=lambda fn: os.path.getmtime(curDir + "\\" + fn)) # 将lists下的所有文件按时间排序
    file_new = lists[-1] # 取最新的文件
    # print(file_new)  
    oldname = os.path.splitext(file_new) # 分离文件名和扩展名 
    # print(oldname)   
    a = str(oldname[0])
    b = a[37:73]
    print("获取到原文件名为：" + a + "......" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    # print(b)
    
    for dirpath, dirnames, filenames in os.walk(curDir):
        # print(dirpath)
        for filename in filenames:
            if filename.find(a) != -1:
                newname = filename.replace(a, b)
                print("已将原文件名：" + filename)
                print("重命名为：" + newname + "......" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                os.rename(os.path.join(dirpath, filename), os.path.join(dirpath, newname))
    
                
def list_dir(path, list_name): 
    """
    返回路径下所有文件和文件名
    将返回的文件和path拼接成绝对路径传给.isdir()判断
    
    """
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if os.path.isdir(file_path):
            list_dir(file_path, list_name)
        else:
             list_name.append((file_path,os.path.getctime(file_path)))
 
 
def newest_file(target_list):
    """
    获取最新的文件
    """
    newest_file = target_list[0]
    for i in range(len(target_list)):
        if i < (len(target_list)-1) and newest_file[1] < target_list[i+1][1]:
            newest_file = target_list[i+1]
        else:
            continue
    print("最新的文件是：" + str(newest_file) + "......" + 
    datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    return newest_file


def move_apk_2_dst():
    """
    将portalWeb下的apk移动到dst暂存
    将portalWeb下的apk直接移动到appd_ata/files/attachments
    """
    list = []
    list_dir(portal_path, list)
    # print(listdir(portal_path, list))
    new_file = newest_file(list)
    print('正在将文件从:', new_file[0] + "......"
    + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    print('移动到:', shutil.copy(new_file[0], dst_path) + "......"
    + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))  # 将压缩包复制到dst，以便后续重命名再复制到packages下
    print('正在将文件从:', new_file[0] + "......"
    + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    print('移动到:', shutil.copy(new_file[0], app_attachments) + "......"
    + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))  # 直接将压缩包复制到appdata/files/attachments下


def move_renamed_apk_2_pack():
    """
    将重命名后的apk复制到app/files/packages下
    """
    list = []
    list_dir(dst_path, list)
    new_file = newest_file(list)
    print('正在将重命名后的文件从:', new_file[0] + "......"
    + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    print('移动到:', shutil.copy(new_file[0], app_packages) + "......"
    + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))  # 将重命名后的压缩包复制到app/packages下
    time.sleep(1)
    print('发布成功……')



if __name__ == '__main__':
    # move_apk_2_dst()
    # time.sleep(1)
    # rename_apk(dst_path)
    # time.sleep(1)
    # move_renamed_apk_2_pack()
    # create_new_version()
    zip_files('C:\\Users\\crmadmin\\Desktop\\dst2')
    
    
    
    
    