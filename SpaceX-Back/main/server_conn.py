# -*- coding:utf-8 -*-
import paramiko

from .logger import info


class SSHConnect(object):

    def __init__(self, hostname, username='crmadmin', password='auxp@ssw0rd', port=22, timeout=10):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.port = port
        self.timeout = timeout

    # 连接服务器
    def connect(self):
        try:
            transport = paramiko.Transport((self.hostname, self.port))
            transport.banner_timeout = self.timeout
            transport.connect(username=self.username, password=self.password)
            self.__transport = transport
            print(info('server connected'))
        except Exception as e:
            print(e)

    # 关闭连接
    def disconnect(self):
        self.__transport.close()
        print(info('server disconnect'))

    # 在远程服务器上执行命令行
    def exec_cmd(self, command):
        ssh = paramiko.SSHClient()
        ssh._transport = self.__transport
        stdin, stdout, stderr = ssh.exec_command(command)
        # print(info('cmd execute done'))
        return stdout.read()
        # print(stdout.read())

    # 上传文件到服务器
    def upload(self, local_path, target_path):
        try:
            print(info('start uploading'))
            sftp = paramiko.SFTPClient.from_transport(self.__transport)
            sftp.put(local_path, target_path)
            print(info('upload finished'))
        except:
            print(info('upload failed'))

    # 从服务器上获取文件
    def download(self, remote_path, local_path):
        try:
            print(info('start downloading'))
            sftp = paramiko.SFTPClient.from_transport(self.__transport)
            sftp.get(remote_path, local_path)
            print(info('download finished'))
        except Exception as e:
            print(e)


# 测试
if __name__  == '__main__':
    pass
    # ssh = SSHConnect(hostname='10.151.66.61', username='crmadmin', password='auxp@ssw0rd')
    # ssh.connect()
    # if not ssh.exec_cmd('cd /cygdrive/d/workspace/AppWeb/debug && rm -rf v2') and ssh.exec_cmd('cd /cygdrive/d/workspace/AppWeb/debug mkdir v2'):
    #     print('failed')
    # else:
    #     print('finished')
    # # ssh.exec_cmd('cd /cygdrive/d/workspace/AppWeb/debug && mkdir v2') print(ssh.exec_cmd('cd
    # # /cygdrive/d/workspace/tmp_files/ && unzip -o angular -d /cygdrive/d/workspace/AppWeb/debug') ssh.exec_cmd('cd
    # # /cygdrive/d/workspace/AppWeb/debug && mkdir v2 && cd /cygdrive/d/workspace/tmp_files/ && unzip -d
    # # /cygdrive/d/workspace/AppWeb/debug/v2 vue.zip') ssh.upload(
    # # '/Users/arthurw/Desktop/doc/python-3.8.4-docs-pdf-a4.zip',
    # # '/cygdrive/d/workspace/python-3.8.4-docs-pdf-a4.zip') ssh.download('/cygdrive/d/workspace/interaction.zip',
    # # '/Users/arthurw/Desktop/doc/docs-pdf/interaction.zip')
    # ssh.disconnect()