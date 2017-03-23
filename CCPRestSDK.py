# -*- coding: UTF-8 -*-
#  Copyright (c) 2014 The CCP project authors. All Rights Reserved.
#
#  Use of this source code is governed by a Beijing Speedtong Information Technology Co.,Ltd license
#  that can be found in the LICENSE file in the root of the web site.
#
#   http://www.yuntongxun.com
#
#  An additional intellectual property rights grant can be found
#  in the file PATENTS.  All contributing project authors may
#  be found in the AUTHORS file in the root of the source tree.

import md5
import base64
import datetime
import urllib2
import json
from xmltojson import xmltojson


class REST:
    
    AccountSid = ''
    AccountToken = ''
    AppId = ''
    SubAccountSid = ''
    SubAccountToken = ''
    ServerIP = ''
    ServerPort = ''
    SoftVersion = ''
    Iflog = True            #是否打印日志
    Batch = ''              #时间戳
    BodyType = 'xml'        #包体格式，可填值：json 、xml

    def __init__(self, ServerIP, ServerPort, SoftVersion):
        """
        初始化

        :param serverIP: 必选参数    服务器地址
        :param serverPort: 必选参数    服务器端口
        :param softVersion: 必选参数    REST版本号
        """
        self.ServerIP = ServerIP
        self.ServerPort = ServerPort
        self.SoftVersion = SoftVersion

    def setAccount(self, AccountSid, AccountToken):
        """
        设置主帐号

        :param AccountSid: 必选参数    主帐号
        :param AccountToken: 必选参数    主帐号Token
        """
        self.AccountSid = AccountSid
        self.AccountToken = AccountToken

    def setSubAccount(self, SubAccountSid, SubAccountToken):
        """
        设置子帐号

        :param SubAccountSid: 必选参数    子帐号
        :param SubAccountToken: 必选参数    子帐号Token
        """
        self.SubAccountSid = SubAccountSid
        self.SubAccountToken = SubAccountToken

    def setAppId(self, AppId):
        """
        设置应用ID

        :param AppId: 必选参数  应用ID
        """
        self.AppId = AppId
    
    def log(self, url, body, data):
        print('这是请求的URL：')
        print (url)
        print('这是请求包体:')
        print (body)
        print('这是响应包体:')
        print (data)
        print('********************************')

    def sendTemplateSMS(self, to, datas, tempId):
        """
        发送模板短信

        :param to: 必选参数     短信接收彿手机号码集合,用英文逗号分开
        :param datas: 可选参数    内容数据
        :param tempId: 必选参数    模板Id
        """
        self.accAuth()
        nowdate = datetime.datetime.now()
        self.Batch = nowdate.strftime("%Y%m%d%H%M%S")
        # 生成sig
        signature = self.AccountSid + self.AccountToken + self.Batch
        sig = md5.new(signature).hexdigest().upper()
        # 拼接URL
        url = "https://{ServerIP}:{ServerPort}/{SoftVersion}/Accounts/{AccountSid}/SMS/TemplateSMS?sig={sig}".format(
            ServerIP=self.ServerIP, ServerPort=self.ServerPort, SoftVersion=self.SoftVersion,
            AccountSid=self.AccountSid, sig=sig)
        # 生成auth
        src = self.AccountSid + ":" + self.Batch
        auth = base64.encodestring(src).strip()
        req = urllib2.Request(url)
        self.setHttpHeader(req)
        req.add_header("Authorization", auth)
        # 创建包体
        b=''
        for a in datas:
            b += '<data>%s</data>' % a
        body = '<?xml version="1.0" encoding="utf-8"?><SubAccount><datas>' + b + '</datas><to>%s</to><templateId>%s' \
                                                                                 '</templateId><appId>%s</appId>' \
                                                                                 '</SubAccount>' % (to, tempId, self.AppId)
        if self.BodyType == 'json':
            b = '['
            for a in datas:
                b += '"%s",' % a
            b += ']'
            body = '''{"to": "%s", "datas": %s, "templateId": "%s", "appId": "%s"}''' % (to, b, tempId, self.AppId)
        req.add_data(body.encode('utf-8'))
        data = ''
        try:
            res = urllib2.urlopen(req)
            data = res.read()
            res.close()
        
            if self.BodyType == 'json':
                locations = json.loads(data)
            else:
                xtj = xmltojson()
                locations = xtj.main(data)
            if self.Iflog:
                self.log(url, body, data)
            return locations
        except Exception, error:
            if self.Iflog:
                self.log(url, body, data)
            return {'172001': '网络错误'}

    def accAuth(self):
        """主帐号鉴权"""
        if self.ServerIP == "":
            print('172004')
            print('IP为空')
        
        if self.ServerPort <= 0:
            print('172005')
            print('端口错误（小于等于0）')
        
        if self.SoftVersion == "":
            print('172013')
            print('版本号为空')
        
        if self.AccountSid == "":
            print('172006')
            print('主帐号为空')
        
        if self.AccountToken == "":
            print('172007')
            print('主帐号令牌为空')
        
        if self.AppId == "":
            print('172012')
            print('应用ID为空')

    def setHttpHeader(self, req):
        """设置包头"""
        if self.BodyType == 'json':
            req.add_header("Accept", "application/json")
            req.add_header("Content-Type", "application/json;charset=utf-8")
            
        else:
            req.add_header("Accept", "application/xml")
            req.add_header("Content-Type", "application/xml;charset=utf-8")