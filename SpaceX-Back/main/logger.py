import datetime
import logging

# 打印当前年月日，时分秒
def info(content):
    return datetime.datetime.now().strftime('[%Y-%m-%d %H:%M:%S]') + ' ======== {}'.format(content)

