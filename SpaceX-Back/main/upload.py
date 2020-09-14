# -*- coding:utf-8 -*-

import requests
import json

from api_test import get_newest_info, get_token
from requests_toolbelt import MultipartEncoder


def upload_zip():
    url = "http://10.151.66.60:8091/api/attachment/upload"
    m = MultipartEncoder(
        fields={'ModuleType': 'version',
                'FileId': '',
                'FileName': 'debug.zip',
                'ObjectId': '{}'.format(get_newest_info(1)),
                'IsOverwrite': '1',
                '': (
                    'debug.zip', open('C:\\Users\\crmadmin\\Desktop\\debug.zip', 'rb'), 'application/x-zip-compressed')}
    )
    header_dic = get_token()
    header_dic["Content-Type"] = "{}".format(m.content_type)
    headers = header_dic
    r = requests.post(url=url, data=m, headers=headers)
    a = r.status_code
    if a == 200:
        print('上传成功')
    else:
        print('上传失败，请重试')


if __name__ == '__main__':
    upload_zip()
