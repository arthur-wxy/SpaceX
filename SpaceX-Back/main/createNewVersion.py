# -*- coding: utf-8 -*-
import datetime
import appFrontEndAutoRelease
import api_test
import requests

def main():
    """app的静态资源发布"""
    appFrontEndAutoRelease.zip_debug('D:\\workspace\\AppWeb\\debug')  # debug下的文件全部打包
    # api_test.get_newest_info() # 传入1返回objectId,传入2返回安卓版本,传入3返回H5版本
    api_test.portal_create(2)  # 创建h5静态资源的最新版本号
    print(datetime.datetime.now().strftime('[%Y-%m-%d %H:%M:%S]') + '======== release finished!')
    # api_test.upload_zip()


if __name__ == '__main__':
    # main()
    appFrontEndAutoRelease.zip_debug('D:\\workspace\\AppWeb\\debug')