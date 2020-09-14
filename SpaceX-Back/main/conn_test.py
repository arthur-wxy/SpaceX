# # coding: utf-8
 
# import paramiko
# import re
# import os
# from time import sleep
 
# # 定义一个类，表示一台远端linux主机

# class Linux(object):
#     # 通过IP, 用户名，密码，超时时间初始化一个远程Linux主机
#     def __init__(self, ip, username, password, timeout=3000):
#         self.ip = ip
#         self.username = username
#         self.password = password
#         self.timeout = timeout
#         # transport和chanel
#         self.t = ''
#         self.chan = ''
#         # 链接失败的重试次数
#         self.try_times = 3
 
#     # 调用该方法连接远程主机
#     def connect(self):
#         while True:
#             # 连接过程中可能会抛出异常，比如网络不通、链接超时
#             try:
#                 self.t = paramiko.Transport(sock=(self.ip, 22))
#                 self.t.connect(username=self.username, password=self.password)
#                 self.chan = self.t.open_session()
#                 self.chan.settimeout(self.timeout)
#                 self.chan.get_pty()
#                 self.chan.invoke_shell()
#                 # 如果没有抛出异常说明连接成功，直接返回
#                 print (u'连接%s成功' % self.ip)
#                 # 接收到的网络数据解码为str
#                 print (self.chan.recv(65535).decode('utf-8'))
#                 return
#             # 这里不对可能的异常如socket.error, socket.timeout细化，直接一网打尽
#             except Exception as e1:
#                 if self.try_times != 0:
#                     print (u'连接%s失败，进行重试' %self.ip)
#                     self.try_times -= 1
#                 else:
#                     print (u'重试3次失败，结束程序')
#                     exit(1)
 
#     # 断开连接
#     def close(self):
#         self.chan.close()
#         self.t.close()
 
#     # 发送要执行的命令
#     def send(self, cmd):
#         cmd += '\r'
#         # 通过命令执行提示符来判断命令是否执行完成
#         p = re.compile(r':~ #')
 
#         result = ''
#         # 发送要执行的命令
#         self.chan.send(cmd)
#         # 回显很长的命令可能执行较久，通过循环分批次取回回显
#         while True:
#             sleep(0.5)
#             ret = self.chan.recv(65535)
#             ret = ret.decode('utf-8')
#             result += ret
#             if p.search(ret):
#                 print (result)
#                 return result
#     # ------获取本地指定目录及其子目录下的所有文件------
#     def __get_all_files_in_local_dir(self, local_dir):
#         # 保存所有文件的列表
#         all_files = list()
 
#         # 获取当前指定目录下的所有目录及文件，包含属性值
#         files = os.listdir(local_dir)
#         for x in files:
#             # local_dir目录中每一个文件或目录的完整路径
#             filename = os.path.join(local_dir, x)
#             # 如果是目录，则递归处理该目录
#             if os.path.isdir(x):
#                 all_files.extend(self.__get_all_files_in_local_dir(filename))
#             else:
#                 all_files.append(filename)
#         return all_files
 
#     def sftp_put_dir(self, local_dir, remote_dir):
#         t = paramiko.Transport(sock=(self.ip, 22))
#         t.connect(username=self.username, password=self.password)
#         sftp = paramiko.SFTPClient.from_transport(t)
 
#         # 去掉路径字符穿最后的字符'/'，如果有的话
#         if remote_dir[-1] == '/':
#             remote_dir = remote_dir[0:-1]
 
#         # 获取本地指定目录及其子目录下的所有文件
#         all_files = self.__get_all_files_in_local_dir(local_dir)
#         # 依次put每一个文件
#         for x in all_files:
#             filename = os.path.split(x)[-1]
#             remote_filename = remote_dir + '/' + filename
#             print (x)
#             print (remote_filename)
#             print (u'Put文件%s传输到%s中...' % (filename,self.ip))
#             sftp.put(x, remote_filename)
# if __name__ == '__main__':
#     # host = Linux('172.16.10.40', 'root', 'imlytek!40')
#     # host.connect()
#     # host.send('ls -l')
#     remote_path = r'/root/test'
#     local_path = r'/Users/arthurw/Desktop/doc/365crm'
#     # host.sftp_put_dir(local_path, remote_path)
#     hostArray=[['120.27.215.130','root','P@ssw0rd']]
#     for x in hostArray:
#       host = Linux(x[0], x[1], x[2])
#       host.sftp_put_dir(local_path, remote_path)
#     #host.close()

import paramiko
import datetime
import os


def upload_all_files(local_dir, remote_dir):
    try:
        t = paramiko.Transport((hostname, port))
        t.connect(username=username, password=password)
        sftp = paramiko.SFTPClient.from_transport(t)
        print('start uploading files {}'.format(datetime.datetime.now()))
        for root, dirs, files in os.walk(local_dir):
            for filespath in files:
                local_file = os.path.join(root, filespath)
                a = local_file.replace(local_dir, '')
                remote_file = os.path.join(remote_dir, a)
                try:
                    sftp.put(local_file, remote_file)
                except Exception as e:
                    sftp.mkdir(os.path.split(remote_file)[0])
                    sftp.put(local_file, remote_file)
                print('upload {} to remote {}'.format(local_file, remote_file))
            for name in dirs:
                local_path = os.path.join(root, name)
                a = local_path.replace(local_dir, '')
                remote_path = os.path.join(remote_dir, a)
                try:
                    sftp.mkdir(remote_path)
                    print('mkdir path {}'.format(datetime.datetime.now()))
                except Exception as e:
                    print(e)
        print('upload files success {}'.format(datetime.datetime.now()))
        t.close()
    except Exception as e:
        print(e)


def conn():
    hostname = '10.151.66.60'
    username = 'crmadmin'
    password = 'auxp@ssw0rd'
    port = 22
    local_dir = '/Users/arthurw/Desktop/doc/test/app.js'
    remote_dir = '/cygdrive/d/workspace/AppWeb-A-8089/app.js'
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=hostname, port=22, username=username, password=password)
    stdin, stdout, stderr = ssh.exec_command('ls -a')
    result = stdout.read()
    print(result)
    # upload_all_files(local_dir, remote_dir)
    

if __name__ == '__main__':
    conn()
    # hostname = '120.27.215.130'
    # username = 'root'
    # password = 'P@ssw0rd'
    # port = 22
    # local_dir = '/Users/arthurw/Desktop/doc/365crm'
    # # remote_dir = '/root/test/'
    # hostname = '10.151.66.60'
    # username = 'crmadmin'
    # password = 'auxp@ssw0rd'
    # port = 22
    # local_dir = '/Users/arthurw/Desktop/doc/test'
    # remote_dir = '/cygdrive/d/workspace/AppWeb-A-8089/test'
    # upload_all_files(local_dir, remote_dir)
    