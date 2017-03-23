# coding=gbk
# coding=utf-8
# -*- coding: UTF-8 -*-

from CCPRestSDK import REST


class Config:

    # ���ʺ�
    accountSid= '�������ʺ�'
    # ���ʺ�Token
    accountToken= '�������ʺ�Token'
    # Ӧ��Id
    appId='����Ӧ��ID'
    # �����ַ����ʽ���£�����Ҫдhttp://
    serverIP='app.cloopen.com'
    # ����˿�
    serverPort='8883'
    # REST�汾��
    softVersion='2013-12-26'


def sendTemplateSMS(to, datas, tempId):
    """
    ����ģ�����

    :param to: �ֻ�����
    :param datas: �������� ��ʽΪ���� ���磺{'12','34'}���粻���滻���� ''
    :param tempId: ģ��Id
    """
    # ��ʼ��REST SDK
    rest = REST(Config.serverIP, Config.serverPort, Config.softVersion)
    rest.setAccount(Config.accountSid, Config.accountToken)
    rest.setAppId(Config.appId)
    
    result = rest.sendTemplateSMS(to,datas,tempId)
    for k,v in result.iteritems(): 
        
        if k=='templateSMS' :
                for k,s in v.iteritems(): 
                    print '%s:%s' % (k, s)
        else:
            print '%s:%s' % (k, v)
    
   
# sendTemplateSMS(�ֻ�����,��������,ģ��Id)