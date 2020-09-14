# -*- coding:utf-8 -*-
import os
import paramiko
import shutil
import time

from logger import info

def sftp_upload_file(host, user, password, server_path, local_path, timeout=10):
    """
    上传文件,不支持文件夹
    :param host: 主机名
    :param user: 用户名
    :param password: 密码
    :param server_path: 远程路径
    :param local_path: 本地路径
    :param timeout: 超时时间(默认)，必须是int类型
    :return: bool
    """
    try:
        t = paramiko.Transport((host, 22))
        t.banner_timeout = timeout
        t.connect(username=user, password=password)
        sftp = paramiko.SFTPClient.from_transport(t)
        sftp.put(local_path, server_path)
        t.close()
        return True
    except Exception as e:
        print(e)
        return False


def zip_dir(name, source_dir, target_dir):
    """
    zip_name: 压缩包名
    source_dir: 要压缩的目录
    """
    target_path = os.path.join(target_dir, '{}'.format(name))
    # print(target_path)
    # target_dir = os.path.join(target_dir, '{}'.format(zip_name))
    shutil.make_archive(target_path, 'zip', root_dir=source_dir)
    print(info('zip generated'))




def upload():
    host = '10.151.66.61'
    user = 'crmadmin'
    password = 'auxp@ssw0rd'
    port = 22
    # cmd = 'cd /cygdrive/d/workspace/AppWeb-A-8089/'
    zip_dir('D:\Source\APP-FrontEnd\HtmlSource_app\h5-v2\dist', 'D:\Source\\tmp_files\debug')  # 要压缩的文件目录

    local_path = 'D:\Source\\tmp_files\debug.zip'
    server_path = '/cygdrive/d/workspace/tmp_files/debug.zip'
    res = sftp_upload_file(host, user, password, server_path, local_path)
    # print(stdout.readlines())
    if not res:
        print("上传文件: %s 失败" % local_path)
    else:
        print("上传文件: %s 成功" % local_path)

        
def unzip():
    host = '10.151.66.61'
    user = 'crmadmin'
    password = 'auxp@ssw0rd'
    port = 22
    # 指定目录下的zip解压到指定目录下
    cmd = 'cd /cygdrive/d/workspace/tmp_files/ && unzip -d /cygdrive/d/workspace/AppWeb/tmp_debug debug.zip'
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    #ssh.connect( hostname ,22, username , password )
    ssh.connect(hostname=host, username=user, password=password, allow_agent=False, look_for_keys=False)
    stdin, stdout, stderr = ssh.exec_command(cmd)
    print(stdout.readlines())
    # ssh.exec_command(cmd1)
    # time.sleep(1)
    # ssh.exec_command(cmd2)
    
    # print(st.readlines())  
    
    ssh.close()
    
def main():
    upload()
    time.sleep(3)
    unzip()

if __name__ == "__main__":
    main()