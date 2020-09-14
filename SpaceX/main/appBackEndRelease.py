import sys
import os
import portalRelease
import time
import datetime


def compile_sln(sln_path):
    """传入解决方案的路径，编译"""
    os.chdir('D:\\vs\Common7\IDE')  # 先进入devenv程序目录
    if os.system('devenv {} /rebuild'.format(sln_path)) == 0:  # 编译整个解决方案
        print(datetime.datetime.now().strftime('[%Y-%m-%d %H:%M:%S]') + '========= Compile Finished!')



if __name__ == '__main__':
    pass
    # compile_sln('D:\Source\APP-BackEnd\DotNetSource\RekTec.Xmobile.sln')
    