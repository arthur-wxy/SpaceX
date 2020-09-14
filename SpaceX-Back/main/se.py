import sys
import time
import os
import shutil

# from selenium import webdriver
# from selenium.webdriver.support.wait import WebDriverWait 
# from selenium.webdriver.support import expected_conditions
# from selenium.webdriver.common.by import By


def main():

	driver = webdriver.Chrome()
	driver.get('http://10.151.66.60:8091/#/login')

	locatorLogin = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[1]/form/div[4]/div[1]/div/div/button')
	try:

		WebDriverWait(driver,20,0.5).until(EC.presence_of_element_located(locatorLogin)) 

		print("登录页面加载出来啦") 

	except:

		print("页面加载失败")

	driver = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[1]/form/div[1]/div/div/input').send_keys('5710048')
	time.sleep(2)
	driver.quit()


def sh_test():
	b = sys.argv[1].split('/', 2)[1]

	print('%s' % b)
	print('{}'.format(b))


def del_dirs(path, file_name):
	print('当前目录下文件及文件夹：%s' % os.listdir(os.getcwd()))
	file_path = path + '\\' + file_name
	os.removedirs(file_path)
	print('当前目录下文件及文件夹：%s' % os.listdir(os.getcwd()))


def del_files(origin_path, file_name):
        """ 删除当前目录下的指定文件及文件夹"""
        for f in file_name:
            filepath = os.path.join(origin_path, f)  # 将文件名映射为绝对路径
            if os.path.isfile(filepath):  # 判断是否文件，是直接删除
                os.remove(filepath)
                print('files' + filepath + ' removed')
            elif os.path.isdir(filepath):  # 若为文件夹，则删除该文件夹及该文件夹下的所有文件
                shutil.rmtree(filepath, True)
                print('files or dirs' + filepath + ' removed')
        # shutil.rmtree(sta_dir, True)  # 最后删除此文件夹
        print('files delete finished')


def get_h5_files():
	return os.listdir('D:\Source\APP-FrontEnd\HtmlSource_app\h5\\build\debug')
	

if __name__ == '__main__':
    #sh_test()
	# del_dirs('D:\\del1', 'del2')
	del_files('D:\del1\del2', get_h5_files())
	# get_h5_files('D:\Source\APP-FrontEnd\HtmlSource_app\h5\\build\debug')
	# get_h5_files()