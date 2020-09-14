# -*- coding:utf-8 -*-
import os
import sys
import time
import datetime
import portalRelease
import appRelease


def build_vue(vue_path):
    """vue项目打包，传入vue项目的路径"""
    os.chdir(vue_path)
    print(datetime.datetime.now().strftime('[%Y-%m-%d %H:%M:%S]') + '======== run dev-build')
    if os.system('npm run build') == 0:
        print(datetime.datetime.now().strftime('[%Y-%m-%d %H:%M:%S]') + '======== vue build complete')


def main():
    """CRM前端发布"""
    portalRelease.git_pull('D:\Source\CRM-FrontEnd')
    time.sleep(3)
    build_vue('D:\Source\CRM-FrontEnd\CRM\Supervise\supervise')
    time.sleep(5)
    # public的发布
    portalRelease.copy_dir('C:\Program Files\Microsoft Dynamics CRM\CRMWeb\ISV\Public\dist',
                            'C:\Program Files\Microsoft Dynamics CRM\CRMWeb\ISV\Public\\bak')  #  删除之前先备份到bak文件夹
    appRelease.del_files('C:\Program Files\Microsoft Dynamics CRM\CRMWeb\ISV\Public\dist')
    time.sleep(3)
    portalRelease.copy_dir('D:\Source\CRM-FrontEnd\CRM\Supervise\supervise\dist',
                            'C:\Program Files\Microsoft Dynamics CRM\CRMWeb\ISV\Public\dist')
    # inspection的发布
    portalRelease.copy_dir('C:\Program Files\Microsoft Dynamics CRM\CRMWeb\ISV\Inspection\static\dist',
                            'C:\Program Files\Microsoft Dynamics CRM\CRMWeb\ISV\Inspection\static\\bak')
    appRelease.del_files('C:\Program Files\Microsoft Dynamics CRM\CRMWeb\ISV\Inspection\static\dist')
    time.sleep(3)
    portalRelease.copy_dir('D:\Source\CRM-FrontEnd\CRM\Supervise\supervise\dist',
                            'C:\Program Files\Microsoft Dynamics CRM\CRMWeb\ISV\Inspection\static\dist')
    print('Finished!')


if __name__ == '__main__':
    main()