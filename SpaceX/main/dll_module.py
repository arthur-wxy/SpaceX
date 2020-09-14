# -*- coding:utf-8 -*-

# app-backend 
mobile_dll = ['RekTec.Xmobile.Biz.Service.dll',
              'RekTec.Xmobile.Biz.dll',
              'RekTec.Xmobile.Model.dll',
              'RekTec.Xmobile.Service.WebApi.dll',
              'RekTec.XStudio.FileStorage.PortalDBFileSystem.dll'
              ]

# portal-backend
portal_dll = ['RekTec.XStudio.Crm.WebApi.dll',
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
               ]


def mobile():
    global mobile_dll
    return mobile_dll

def portal():
    global portal_dll
    return portal_dll
