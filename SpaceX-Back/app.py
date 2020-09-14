import logging
import os
import json
import time
import yaml


from flask import Flask
from flask import request
from flask import redirect
from flask import jsonify
from flask_cors import *


app = Flask(__name__)
CORS(app, supports_credentials=True)


@app.route('/api/v1/startDeploy', methods=['GET', 'POST'])
def start_deploy():
    if request.method == 'POST':
        a = request.get_data()
        dict1 = json.loads(a)
        # print(dict1)
        client = dict1['client']
        server = dict1['server']
        file = dict1['file']
        branch = dict1['branch']
        print(client, server, file, branch)
        if client == 'appfront':
            if server == 'app1':
                pass
            else:
                time.sleep(3)
                return {'stateCode': '202', 'Msg': 'fail', 'client': '{}'.format(client)}
        elif client == 'appback':
            return {'stateCode': '200', 'Msg': 'success', 'client': '{}'.format(client)}
        elif client == 'portalfront':
            return {'stateCode': '200', 'Msg': 'success', 'client': '{}'.format(client)}
        elif client == 'portalback':
            return {'stateCode': '200', 'Msg': 'success', 'client': '{}'.format(client)}
        else:
            return {'stateCode': '203', 'Msg': 'fail', 'client': 'no such client'}

        # elif client == 'appfront':
        #     return {'stateCode': '200', 'Msg': 'success', 'client': '{}'.format(client)}
        # else:
        #     return {'stateCode': '201', 'Msg': 'fail', 'client': '{}'.format(client)}

            # if client == 'appfront':
            #     return {'stateCode': '200', 'Msg': 'success', 'client': '{}'.format(client)}
            # else:
            #     return {'stateCode': '201', 'Msg': 'fail', 'client': '{}'.format(client)}


        # print('client is : {}'.format(client))
        # print('server1 is : {}'.format(server1))
        # print('server2 is : {}'.format(server2))


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
                     'RekTec.XStudio.Exam.WebApi.dll',
                     'RekTec.XStudio.Parts.Biz.dll',
                     'RekTec.XStudio.Parts.WebApi.dll',
                     'RekTec.XStudio.Public.WebApi.dll',
                     'RekTec.XStudio.Service.Biz.dll',
                     'RekTec.XStudio.Service.WebApi.dll',
                     'RekTec.XStudio.Station.WebApi.dll',
                     'RekTec.XStudio.Station.Biz.dll'
                     ],
                'server':
                    ['portal1',
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
    app.run(debug=True)
