import logging
import os
import json
import time
import datetime
import yaml

from flask import Flask
from flask import request
from flask import redirect
from flask import jsonify
from flask_cors import *
from wsgiref.simple_server import make_server
from main.server_conn import SSHConnect
from main.para_test import zip_dir
from main.appBackEndRelease import compile_sln
from main.appBackUpload import copy_dll

app = Flask(__name__)
CORS(app, supports_credentials=True)


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='D:\source\SpaceX\SpaceX-Back\main\log\\release.log',
                    filemode='a')


def code_pull(repo_path, branch):
    """
    :param repo_path: 项目的本地仓库路径
    :param branch: 要拉取的分支
    :return:
    """
    os.chdir(repo_path)
    os.system('git pull')
    b = branch.replace(' ', '')  # 如果输入的分支含有空格，去除
    if os.system('git clean -n') == 0:  # 避免因冲突产生无法创建分支的情况，先clean没跟踪的文件
        os.system('git clean -f')
    os.system('git checkout -b {} origin/{} '.format(b, b))  # 每次从远程创建最新分支
    print(datetime.datetime.now().strftime('[%Y-%m-%d %H:%M:%S]') + '======== branch created')
    logging.info('branch created')
    os.system('git pull')  # 创建完拉取一下最新分支


def portal_back_release(server_list, branch, dll_list):
    """

    :param server_list: 要发布的服务器列表
    :param branch: 要发布的分支
    :param dll_list: 要发布的dll列表
    :return:
    """
    # 先读一下配置文件，获取路径dll等
    with open('./config/config.yaml', 'r', encoding='UTF-8') as f:
        a = yaml.load(f.read(), Loader=yaml.FullLoader)
        repo_path = a['path']['portal_back_path']
        sln_path = a['path']['portal_sln_path']
        dll_path = a['path']['portal_dll_path']
        portal_tmp_path = a['path']['portal_dll_tmp_path']
        tmp_files_path = a['path']['tmp_files_path']
        portal_back_src_path = a['path']['portal_back_src_path']
        portal_back_dst_path = a['path']['portal_back_dst_path']
        unzip_portal_cmd = a['cmd']['cmd1']

    # 拉取代码
    code_pull(repo_path, branch)
    time.sleep(1)
    # 后端编译
    compile_sln(sln_path)
    time.sleep(1)
    # 复制到临时目录
    copy_dll(dll_path, portal_tmp_path, dll_list)
    #  将此dll目录打包
    zip_dir('PBackRelease', portal_tmp_path, tmp_files_path)
    # 实例化连接，连接服务器
    for i in server_list:
        try:
            s = SSHConnect(hostname=i)
            s.connect()
            s.upload(portal_back_src_path, portal_back_dst_path)
            s.exec_cmd(unzip_portal_cmd)
            s.disconnect()
        except Exception as e:
            print(e)


@app.route('/api/v1/startDeploy', methods=['GET', 'POST'])
def start_deploy():
    if request.method == 'POST':
        a = request.get_data()
        dict1 = json.loads(a)
        # print(dict1)
        client = dict1['client']
        server_list = dict1['server']
        file_list = dict1['file']
        branch = dict1['branch']
        print(client, server_list, file_list, branch)
        if client == 'appfront':
            try:
                # portalBackRelease()
                time.sleep(10)
                return {'stateCode': '200', 'Msg': 'success', 'client': '{}'.format(client)}
            except:
                return {'stateCode': '202', 'Msg': 'failed', 'client': '{}'.format(client)}
        elif client == 'appback':
            return {'stateCode': '200', 'Msg': 'success', 'client': '{}'.format(client)}
        elif client == 'portalfront':
            return {'stateCode': '200', 'Msg': 'success', 'client': '{}'.format(client)}
        elif client == 'portalback':
            try:
                portal_back_release(server_list, branch, file_list)
                # print(portal_back_release(server_list, branch, file_list))
                # logging.info(portal_back_release(server_list, branch, file_list))
                # test()
                return {'stateCode': '200', 'Msg': 'success', 'client': '{}'.format(client)}
            except:
                return {'stateCode': '202', 'Msg': 'fail', 'client': '{}'.format(client)}
        else:
            return {'stateCode': '203', 'Msg': 'fail', 'client': 'no such client'}

    else:
        return {'只接受post请求!'}


@app.route('/api/v1/getFilesList')
def get_files():
    client = request.args.get("client")
    # print(client)
    # print(type(client))
    if client == 'appback':
        return {'data':
                    ['RekTec.Xmobile.Biz.Service.dll',
                     'RekTec.Xmobile.Biz.dll',
                     'RekTec.Xmobile.Model.dll',
                     'RekTec.Xmobile.Service.WebApi.dll',
                     'RekTec.XStudio.FileStorage.PortalDBFileSystem.dll'
                     ],
                'server':
                    ['app1',
                     'app2',
                     'app3',
                     'app4'
                     ]
                }
    elif client == 'portalback':
        return {'data':
                    ['RekTec.XStudio.Crm.WebApi.dll',
                     'RekTec.XStudio.Exam.WebApi.dll',
                     'RekTec.XStudio.Expense.Biz.dll',
                     'RekTec.XStudio.Parts.Biz.dll',
                     'RekTec.XStudio.Parts.WebApi.dll',
                     'RekTec.XStudio.Public.WebApi.dll',
                     'RekTec.XStudio.Service.Biz.dll',
                     'RekTec.XStudio.Service.WebApi.dll',
                     'RekTec.XStudio.Station.WebApi.dll',
                     'RekTec.XStudio.Station.Biz.dll'
                     ],
                'server':
                    ['10.151.66.60',
                     'portal2',
                     'portal3',
                     'portal4'
                     ]
                }
    elif client == 'appfront':
        return {'data':
                    ['angular',
                     'vue'
                     ],
                'server':
                    ['app1',
                     'app2',
                     'app3',
                     'app4'
                     ]
                }

    elif client == 'portalfront':
        return {'data': ['vue'],
                'server':
                    ['portal1',
                     'portal2',
                     'portal3',
                     'portal4'
                     ]
                }
    else:
        return {'Msg': ['no such client']}


@app.route('/user/<name>')
def user(name):
    return '<h1>hello, %s</h1>' % name


if __name__ == '__main__':
    # server = make_server('127.0.0.1', 5000, app)
    # server.serve_forever()
    # app.run()
    app.run(debug=True)
