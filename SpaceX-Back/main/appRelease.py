# -*- coding:utf-8 -*-
import os
import datetime
import time
import shutil
import sys


def build_vue(vue_path):
    """vue项目打包，传入vue项目的路径"""
    os.chdir(vue_path)
    print(datetime.datetime.now().strftime('[%Y-%m-%d %H:%M:%S]') + '======== run dev-build')
    if os.system('npm run build') == 0:
        print(datetime.datetime.now().strftime('[%Y-%m-%d %H:%M:%S]') + '======== vue build complete')


def build_h5(h5_path):
    """h5项目打包，传入h5的路径"""
    os.chdir(h5_path)
    # print(datetime.datetime.now().strftime('[%Y-%m-%d %H:%M:%S]') + '======== run gulp')
    # os.system('pwd')
    os.system('start gulp')  # 带上&就能退出外部命名的子进程！！！！！
    # 在Windows下，用DOS的start命令通常也能使命令并行启动：os.system('start python test.py ')
    time.sleep(3)
    print(datetime.datetime.now().strftime('[%Y-%m-%d %H:%M:%S]') + '======== h5 build complete')


def time_logging(func):
    def wrapper(*args):
        print(datetime.datetime.now().strftime('[%Y-%m-%d %H:%M:%S]') + '======== deleting files')
        func(*args)
        print(datetime.datetime.now().strftime('[%Y-%m-%d %H:%M:%S]') + '======== delete finished')

    return wrapper


@time_logging
def del_files(origin_path):
    """ 删除当前目录下的指定文件及文件夹"""
    # if os.path.exists('{}\index.html'.format(origin_path)):
    #     os.remove('{}\index.html'.format(origin_path))
    # print('index文件已移除')
    # file_list = []
    # sta_dir = '{}\\v2'.format(origin_path)
    file_list = os.listdir(origin_path)  # 列出该目录下的所有文件名
    for f in os.listdir(origin_path):
        filepath = os.path.join(origin_path, f)  # 将文件名映射为绝对路径
        if os.path.isfile(filepath):  # 判断是否文件，是直接删除
            os.remove(filepath)
            print('file' + filepath + ' removed')
        elif os.path.isdir(filepath):  # 若为文件夹，则删除该文件夹及该文件夹下的所有文件
            shutil.rmtree(filepath, True)
            print('dir' + filepath + ' removed')
    # shutil.rmtree(sta_dir, True)  # 最后删除此文件夹
    print('files delete finished')


def del_file(origin_path, file_name):
        """ 删除当前目录下的指定文件及文件夹, 上面的del_files待重写"""
        for f in file_name:
            filepath = os.path.join(origin_path, f)  # 将文件名映射为绝对路径
            if os.path.isfile(filepath):  # 判断是否文件，是直接删除
                os.remove(filepath)
                print('files' + filepath + ' removed')
            elif os.path.isdir(filepath):  # 若为文件夹，则删除该文件夹及该文件夹下的所有文件
                shutil.rmtree(filepath)
                print('files or dirs' + filepath + ' removed')
            else:
                print('files or file does not exsit')
        # shutil.rmtree(sta_dir, True)  # 最后删除此文件夹
        


def get_h5_files_list():
	return os.listdir('D:\Source\APP-FrontEnd\HtmlSource_app\h5\\build\debug')


def main():
    """app拉取代码，打包，发布"""
    portalRelease.git_pull('D:\Source\APP-FrontEnd')
    time.sleep(3)
    build_vue('D:\Source\APP-FrontEnd\HtmlSource_app\h5-v2')
    build_h5('D:\Source\APP-FrontEnd\HtmlSource_app\h5')
    time.sleep(30)  # 等待gulp执行完,h5有个controler.js生成时间大约30s，所以等待30s
    del_files('D:\workspace\AppWeb\debug\\v2')
    time.sleep(3)
    del_file('D:\\workspace\\AppWeb\\debug', get_h5_files_list())
    time.sleep(3)
    portalRelease.copy_dir('D:\\Source\\APP-FrontEnd\\HtmlSource_app\\h5-v2\\dist',
                           'D:\\workspace\\AppWeb\\debug\\v2')
    portalRelease.copy_dir('D:\\Source\\APP-FrontEnd\\HtmlSource_app\\h5\\build\\debug',
                            'D:\\workspace\\AppWeb\\debug')
    print('Finished!')


if __name__ == '__main__':
    main()
    #del_file('D:\Source\\test', get_h5_files_list())
    #build_h5('D:\Source\APP-FrontEnd\HtmlSource_app\h5')