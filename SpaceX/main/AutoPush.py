import os
import time

from logger import cur_time
from portalRelease import git_pull

"""
集团GitLab的仓库地址：


http://10.88.21.45/jduser-css/crm-frontend.git  

http://10.88.21.45/jduser-css/app-backend.git

http://10.88.21.45/jduser-css/Ayf.Css.Base.git

http://10.88.21.45/jduser-css/app-ios.git

http://10.88.21.45/jduser-css/CC-FrontEnd.git

http://10.88.21.45/jduser-css/crm-backend.git

http://10.88.21.45/jduser-css/portal-frontend.git

http://10.88.21.45/jduser-css/WeChat400-FrontEnd.git

http://10.88.21.45/jduser-css/ocelotgetway.git

http://10.88.21.45/jduser-css/workorderwebapi.git

http://10.88.21.45/jduser-css/portal-backend.git

http://10.88.21.45/jduser-css/wechat400-backend.git

http://10.88.21.45/jduser-css/css-common.git

http://10.88.21.45/jduser-css/auxcss.service.git

http://10.88.21.45/jduser-css/homesmartapi.git

http://10.88.21.45/jduser-css/app-android.git

http://10.88.21.45/jduser-css/crm.git

http://10.88.21.45/jduser-css/aux-integration-service.git

http://10.88.21.45/jduser-css/APP-FrontEnd.git

http://10.88.21.45/jduser-css/portal.git

http://10.88.21.45/jduser-css/CSS.Front-End.SourceCode.git

http://10.88.21.45/jduser-css/common.git
"""

def main():
    
