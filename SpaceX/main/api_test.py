# -*- coding:utf-8 -*-

import json
import time
import datetime
import requests

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from requests_toolbelt import MultipartEncoder
from appFrontEndAutoRelease import zip_and_move, zip_debug


def get_token():
    """获取token"""
    url = "http://10.151.66.60:8091/Token"
    m = ({'grant_type': 'password',
          'username': 'admin',
          'password': 'P@ssw0rd'
          })
    r = requests.post(url=url, data=m)
    access_token = r.json()['access_token']
    headers = {"Authorization": "Bearer {}".format(access_token)}
    return headers


def get_newest_info(query_type):
    """
    传入1返回objectId
    传入2返回加1后的安卓版本
    传入3返回加1后的H5版本
    """
    url = "http://10.151.66.60:8091/api/PortalVersion/AllVersion/1/50"
    headers = get_token()
    r = requests.get(url=url, headers=headers)
    new_list = json.loads(r.text)  # 将返回的内容转成python对象
    new_dic = new_list['Data']['DataList']  # 取出列表中的字典
    if query_type == 1:
        object_id = new_list['Data']['DataList'][0]['id']
        return object_id
    elif query_type == 2:
        cur_android_version = sorted(new_dic, key=lambda i: i['clientType'])[0]['versionCode']
        cur_text = cur_android_version.split('.', 3)  # 拆分版本号
        n1 = cur_text[0]
        n2 = cur_text[1]
        n3 = int(cur_text[2]) + 1  # 取出第三位+1
        n4 = cur_text[3]
        new_android_version = n1 + '.' + n2 + '.' + str(n3) + '.' + n4  # 重新拼接
        return new_android_version
    elif query_type == 3:
        cur_h5_version = sorted(new_dic, key=lambda i: i['clientType'], reverse=True)[0]['versionCode']
        cur_text = cur_h5_version.split('.', 3)
        n1 = cur_text[0]
        n2 = cur_text[1]
        n3 = cur_text[2]
        n4 = int(cur_text[3]) + 1  # 取出第四位+1
        new_h5_version = n1 + '.' + n2 + '.' + n3 + '.' + str(n4)  # 重新拼接
        return new_h5_version


def portal_create(client_type):
    """
    type=1时创建安卓
    type=2时创建h5
    """
    driver = webdriver.Chrome(r'D:\python\Lib\site-packages\selenium\webdriver\\chromedriver.exe')
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

    if client_type == 1:
        # 选择android版本
        mouse = driver.find_element_by_xpath("/html/body/div[3]/div/div[1]/ul/li[1]/span")
        ActionChains(driver).move_to_element(mouse).click().perform()
        time.sleep(1)
        driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div[2]/div/div[5]/div/div/div[2]/form/div[1]\
        /div[2]/div/div/div[1]/input").send_keys("{}".format(get_newest_info(2)))
        time.sleep(1)
        # 输入说明
        driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div[2]/div/div[5]/div/div/div[2]/form/div[2]\
        /div/div/div/div/input").send_keys("{}".format(get_newest_info(2)))
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

    elif client_type == 2:
        # 选择h5版本
        mouse = driver.find_element_by_xpath("/html/body/div[3]/div/div[1]/ul/li[3]/span")
        ActionChains(driver).move_to_element(mouse).click().perform()
        time.sleep(1)
        # 输入版本号
        driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div[2]/div/div[5]/div/div/div[2]/form/div[1]\
        /div[2]/div/div/div[1]/input").send_keys("{}".format(get_newest_info(3)))
        time.sleep(1)
        # 输入说明
        driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div[2]/div/div[5]/div/div/div[2]/form/div[2]\
        /div/div/div/div/input").send_keys("{}".format(get_newest_info(3)))
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
        # 文件上传成功后，刷新页面，重新进入该记录，发布，关闭浏览器
        upload_zip()
        time.sleep(5)
        zip_and_move()
        time.sleep(5)
        driver.find_element_by_class_name("el-dialog__headerbtn").click()
        time.sleep(2)
        # driver.find_element_by_class_name("el-table_1_column_3").double
        dc = driver.find_element_by_xpath(
            "/html/body/div[1]/div/div[2]/div[2]/div/div[3]/div/div[3]/table/tbody/tr[1]/td[3]/div")
        ActionChains(driver).double_click(dc).perform()
        time.sleep(7)
        driver.find_element_by_xpath(
            "/html/body/div[1]/div/div[2]/div[2]/div/div[5]/div/div/div[2]/div/button[3]/span").click()
        time.sleep(5)
        driver.close()


class SendRequest:

    def __init__(self, url, method, token):
        self.url = url
        self.method = method
        self.token = token

    # def get_response(self):
    #     if self.method == 'GET':
    #         self.send_get_request
    #     elif self.method == 'POST':
    #         self.send_post_request

    def send_get_request(self):
        r = requests.get(url=self.url, headers=get_token())
        new_dic = json.loads(r.text)
        return new_dic

    def send_post_request(self):
        r = requests.post(url=self.url, headers=get_token())


def upload_zip():
    url = "http://10.151.66.60:8091/api/attachment/upload"
    m = MultipartEncoder(
        fields={'ModuleType': 'version',
                'FileId': '',
                'FileName': 'debug.zip',
                'ObjectId': '{}'.format(get_newest_info(1)),
                'IsOverwrite': '1',
                '': (
                'debug.zip', open('D:\\workspace\\AppWeb\\debug\\debug.zip', 'rb'), 'application/x-zip-compressed')}
    )
    header_dic = get_token()
    header_dic["Content-Type"] = "{}".format(m.content_type)
    headers = header_dic
    r = requests.post(url=url, data=m, headers=headers)
    a = r.status_code
    if a == 200:
        print(datetime.datetime.now().strftime('[%Y-%m-%d %H:%M:%S]') + '======== update success')
    else:
        print(datetime.datetime.now().strftime('[%Y-%m-%d %H:%M:%S]') + '======== update failed')


if __name__ == "__main__":
    # portal_api_test()
    # api_upload_files()
    # code = 1
    # get_newest_info(3)
    zip_debug()
    portal_create(2)
