# -*- coding: utf-8 -*-
import sys
import os.path

app_root = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(app_root, 'site-packages'))
sys.path.insert(0, os.path.join(app_root, "web"))

class Borg():
    '''base http://blog.youxu.info/2010/04/29/borg
        - 单例式配置收集类
    '''
    __collective_mind = {}
    def __init__(self):
        self.__dict__ = self.__collective_mind

    TPL_TEXT=''' <xml>
     <ToUserName><![CDATA[%(toUser)s]]></ToUserName>
     <FromUserName><![CDATA[%(fromUser)s]]></FromUserName>
     <CreateTime>%(tStamp)s</CreateTime>
     <MsgType><![CDATA[text]]></MsgType>
     <Content><![CDATA[%(content)s]]></Content>
     </xml>'''

CFG = Borg()

