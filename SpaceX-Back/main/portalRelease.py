# -*- coding:utf-8 -*-
import os
import datetime
import time
import shutil
import sys


def build_vue(vue_path):
    """vue项目打包，传入vue项目的路径"""
    os.chdir(vue_path)
    print(datetime.datetime.now().strftime('[%Y-%m-%d %H:%M:%S]') + '======== run dev-build')
    if os.system('npm run dev-build') == 0:
        print(datetime.datetime.now().strftime('[%Y-%m-%d %H:%M:%S]') + '======== vue build complete')


def build_h5(h5_path):
    """h5项目打包，传入h5的路径"""
    os.chdir(h5_path)
    print(datetime.datetime.now().strftime('[%Y-%m-%d %H:%M:%S]') + '======== run gulp')
    os.system('start gulp')  # 类linux的带上&就能退出外部命名的子进程！！！！！
    # 在Windows下，用DOS的start命令通常也能使命令并行启动：os.system('start python test.py ')
    time.sleep(3)
    print(datetime.datetime.now().strftime('[%Y-%m-%d %H:%M:%S]') + '======== h5 build complete')


class PullAndBuild:
    """
    获取最新的bug分支，打包后复制到目标文件夹
    branch: 最新的分支
    project_type: CRM 0/APP 1/portal 3
    source_path：需要打包项目的路径
    target_path: 需要发布的目标路径
    origin_path: 原先项目下的文件路径，如app下的vue项目，用于删除原文件
    build_path: 前端打完包之后的文件路径，用于拷贝到target_path
    """

    def __init__(self, branch, project_type, source_path, target_path, origin_path, build_path):
        self.branch = branch
        self.project_type = project_type
        self.source_path = source_path
        self.target_path = target_path
        self.origin_path = origin_path
        self.build_path = build_path

    def check_repo_and_pull(self):
        """
        0,1,2 CRM APP PORTAL
        切换最新分支且拉取最新代码
        """
        crm_path = 'D:\Source\CRM-FrontEnd\CRM\Supervise\supervise'
        app_path = '/Users/arthurw/Desktop/source/APP-FrontEnd'
        portal_path = 'D:\Source\Portal-FrontEnd'
        if self.project_type == 0:
            os.chdir(crm_path)
            if os.system('git checkout {}'.format(self.branch)) == 0:
                print(datetime.datetime.now().strftime('[%Y-%m-%d %H:%M:%S]') + '======== 已切换到最新的分支')
                if os.system('git pull') == 0:
                    print(datetime.datetime.now().strftime('[%Y-%m-%d %H:%M:%S]') + '======== 代码已更新')
        elif self.project_type == 1:
            os.chdir(app_path)
            if os.system('git checkout {}'.format(self.branch)) == 0:
                print(datetime.datetime.now().strftime('[%Y-%m-%d %H:%M:%S]') + '======== 已切换到最新的分支')
                if os.system('git pull') == 0:
                    print(datetime.datetime.now().strftime('[%Y-%m-%d %H:%M:%S]') + '======== 代码已更新')
        elif self.project_type == 2:
            os.chdir(portal_path)
            if os.system('git checkout {}'.format(self.branch)) == 0:
                print(datetime.datetime.now().strftime('[%Y-%m-%d %H:%M:%S]') + '======== 已切换到最新的分支')
                if os.system('git pull') == 0:
                    print(datetime.datetime.now().strftime('[%Y-%m-%d %H:%M:%S]') + '======== 代码已更新')

    def npm_build(self):
        """传入source_path 打包前端项目"""
        os.chdir(self.source_path)
        print(datetime.datetime.now().strftime('[%Y-%m-%d %H:%M:%S]') + '======== run build')
        if os.system('npm run build') == 0:
            print(datetime.datetime.now().strftime('[%Y-%m-%d %H:%M:%S]') + '======== vue build complete')

    def time_logging(func):
        def wrapper(*args):
            print(datetime.datetime.now().strftime('[%Y-%m-%d %H:%M:%S]') + '======== start deleting files')
            func(*args)
            print(datetime.datetime.now().strftime('[%Y-%m-%d %H:%M:%S]') + '======== delete finished')

        return wrapper

    @time_logging
    def del_files(self):
        """ 删除当前目录下的指定文件及文件夹"""
        if os.path.exists('{}\index.html'.format(self.origin_path)):
            os.remove('{}\index.html'.format(self.origin_path))
            # print('index文件已移除')
        # file_list = []
        sta_dir = '{}\static'.format(self.origin_path)
        file_list = os.listdir(sta_dir)  # 列出该目录下的所有文件名
        for f in os.listdir(sta_dir):
            filepath = os.path.join(sta_dir, f)  # 将文件名映射为绝对路径
            if os.path.isfile(filepath):  # 判断是否文件，是直接删除
                os.remove(filepath)
                print('file' + filepath + ' removed')
            elif os.path.isdir(filepath):  # 若为文件夹，则删除该文件夹及该文件夹下的所有文件
                shutil.rmtree(filepath, True)
                print('dir' + filepath + ' removed')
        shutil.rmtree(sta_dir, True)  # 最后删除此文件夹
        print('files delete finished')

    def move_2_dst(self, name, back_name):
        """ 将打包完毕的文件复制到指定目录下"""
        sys.setrecursionlimit(100000)  # 最大递归深度设置
        for f in os.listdir(self.build_path):
            name = os.path.join(self.build_path, f)  # 文件名映射绝对路径
            back_name = os.path.join(self.target_path, f)
            if os.path.isfile(name):
                if os.path.isfile(back_name):
                    shutil.copy(name, back_name)
                else:
                    shutil.copy(name, back_name)
            else:
                if not os.path.isdir(back_name):  # 如果目标目录不存在此文件夹，创建
                    os.makedirs(back_name)
                self.move_2_dst(name, back_name)


def logging(func):
    def wrapper(*args):
        print(datetime.datetime.now().strftime('[%Y-%m-%d %H:%M:%S]') + '======== start copying files')
        func(*args)
        print(datetime.datetime.now().strftime('[%Y-%m-%d %H:%M:%S]') + '======== released!')
    return wrapper


@logging
def move_2_dst(build_path, target_path):
    """ 将打包完毕的文件复制到指定目录下"""
    sys.setrecursionlimit(100000)  # 最大递归深度设置
    for f in os.listdir(build_path):
        name = os.path.join(build_path, f)  # 文件名映射绝对路径
        back_name = os.path.join(target_path, f)
        if os.path.isfile(name):
            if os.path.isfile(back_name):
                shutil.copy(name, back_name)
            else:
                shutil.copy(name, back_name)
        elif not os.path.isdir(back_name):
            os.makedirs(back_name)
            move_2_dst(name, back_name)

@logging
def copy_dir(build,target):

    '''将一个目录下的全部文件和目录,完整地<拷贝并覆盖>到另一个目录'''
    if not (os.path.isdir(build) and os.path.isdir(target)):
        # 如果传进来的不是目录
        # print("传入目录不存在")
        return

    for a in os.walk(build):
        #递归创建目录
        for d in a[1]:
            dir_path = os.path.join(a[0].replace(build, target), d)
            if not os.path.isdir(dir_path):
                os.makedirs(dir_path)
        #递归拷贝文件
        for f in a[2]:
            dep_path = os.path.join(a[0],f)
            arr_path = os.path.join(a[0].replace(build, target), f)
            shutil.copy(dep_path,arr_path)


def check_repo_and_pull(branch, project_type):
    """
    0,1,2 CRM APP PORTAL
    切换最新分支且拉取最新代码
    3 APP后端
    """
    crm_path = 'D:\Source\CRM-FrontEnd\CRM\Supervise\supervise'
    app_path = 'D:\Source\APP-FrontEnd\HtmlSource_app'
    portal_path = 'D:\Source\Portal-FrontEnd'
    app_back_end_path = 'D:\Source\APP-BackEnd'
    if project_type == 0:
        # crm前端
        os.chdir(crm_path)
        if os.system('git checkout {}'.format(branch)) == 0:
            print(datetime.datetime.now().strftime('[%Y-%m-%d %H:%M:%S]') + '======== 已切换到最新的分支')
            if os.system('git pull') == 0:
                print(datetime.datetime.now().strftime('[%Y-%m-%d %H:%M:%S]') + '======== 代码已更新')
    elif project_type == 1:
        # app前端
        os.chdir(app_path)
        # if os.system('git checkout {}'.format(branch)) == 0:
        #     print(datetime.datetime.now().strftime('[%Y-%m-%d %H:%M:%S]') + '======== 已切换到最新的分支')
        #     if os.system('git pull') == 0:
        #         print(datetime.datetime.now().strftime('[%Y-%m-%d %H:%M:%S]') + '======== 代码已更新')
        # 不管分支是否最新，都先清除branch的本地分支
        os.system('git branch -d {}'.format(branch))
        print(datetime.datetime.now().strftime('[%Y-%m-%d %H:%M:%S]') + '======== processing')
        if os.system('git checkout -b {} origin/{} '.format(2, branch)) == 0:
            print(datetime.datetime.now().strftime('[%Y-%m-%d %H:%M:%S]') + '======== branch created')
            os.system('git pull')
            print(datetime.datetime.now().strftime('[%Y-%m-%d %H:%M:%S]') + '======== updated')


    elif project_type == 2:
        # portal前端
        os.chdir(portal_path)
        if os.system('git checkout {}'.format(branch)) == 0:
            print(datetime.datetime.now().strftime('[%Y-%m-%d %H:%M:%S]') + '======== 已切换到最新的分支')
            if os.system('git pull') == 0:
                print(datetime.datetime.now().strftime('[%Y-%m-%d %H:%M:%S]') + '======== 代码已更新')
    elif project_type == 3:
        # app后端
        os.chdir(app_back_end_path)
        if os.system('git checkout {}'.format(branch)) == 0:
            print(datetime.datetime.now().strftime('[%Y-%m-%d %H:%M:%S]') + '======== 已切换到最新的分支')
            if os.system('git pull') == 0:
                print(datetime.datetime.now().strftime('[%Y-%m-%d %H:%M:%S]') + '======== 代码已更新')


def git_pull(repo_path):
    """git拉取代码的操作
    crm_path = 'D:\Source\CRM-FrontEnd\CRM\Supervise\supervise'
    app_path = 'D:\Source\APP-FrontEnd\HtmlSource_app'
    portal_path = 'D:\Source\Portal-FrontEnd'
    app_back_end_path = 'D:\Source\APP-BackEnd'
    """
    os.chdir(repo_path)
    os.system('git pull')
    b = sys.argv[1].split('/', 2)[1]
    if os.system('git clean -n') == 0:  # 避免因冲突产生无法创建分支的情况，先clean没跟踪的文件
        os.system('git clean -f')
    os.system('git checkout -b {} origin/{} '.format(b, b))  # 每次从远程创建最新分支
    print(datetime.datetime.now().strftime('[%Y-%m-%d %H:%M:%S]') + '======== branch created')
    os.system('git pull')  # 创建完拉取一下最新分支
    

def main():
    """portal拉取前端代码，打包，发布"""
    c = PullAndBuild('200623feature-TEST',
                    '2',
                    'D:\Source\Portal-FrontEnd\h5',
                    'D:\workspace\PortalWeb',
                    'D:\workspace\PortalWeb',
                    'D:\Source\Portal-FrontEnd\h5')  # 实例化
    git_pull('D:\Source\Portal-FrontEnd')
    time.sleep(3)
    c.npm_build()  # 前端资源打包
    c.del_files()  # 删除目标文件index.html static
    time.sleep(3)
    copy_dir('D:\Source\Portal-FrontEnd\h5\\build', 'D:\workspace\PortalWeb')  # 将打完包的文件复制到portalweb下
    print('Finished!')


if __name__ == '__main__':
    main()  # portal发布主函数
    # build_h5('D:\\Source\\APP-FrontEnd\\HtmlSource_app\\h5')
    # move_2_dst('C:\\Users\\crmadmin\\Desktop\\dst', 'C:\\Users\\crmadmin\\Desktop\\dst2')
    # c = PullAndBuild('-b 200623feature-TEST origin/200623feature-TEST',
    #                 '2',
    #                 'D:\Source\Portal-FrontEnd\h5',
    #                 'D:\workspace\PortalWeb',
    #                 'D:\workspace\PortalWeb',
    #                 'D:\Source\Portal-FrontEnd\h5')
    # c.del_files()
    # main()
    # c.check_repo_and_pull()
    # check_repo_and_pull('-b 200623bugfix-TEST origin/200623bugfix-TEST', 2)
    # c = PullAndBuild('1', '2', '3', '/Users/arthurw/Desktop/t1/t4/',
    #                  '/Users/arthurw/Desktop/t1/t4/',
    #                  '/Users/arthurw/Desktop/t1/t5/')
    # c.move_2_dst('', '')
    # getGitfile()
    # check_repo('200623feature-TEST')
    # build_vue('/Users/arthurw/Desktop/source/app-frontend/HtmlSource_app/h5-v2')
    # build_h5('/Users/arthurw/Desktop/source/app-frontend/HtmlSource_app/h5')
    # Check('200623feature-TEST')
    #test()
