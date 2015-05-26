# -*- coding: utf-8 -*-
import sae
import time
from bottle import *
from config import CFG

#from wechat_sdk.basic import WechatBasic
#from xml import etree
#from xml.etree import ElementTree
import xml.etree.ElementTree as ET

#debug(True)
APP = Bottle()
import sae.kvdb
KV = sae.kvdb.KVClient()

@APP.get('/')
def web_access():
     return "bookgiver:share books with others"



@APP.get('/echo/')
def checkSignature():
    print request.query.keys()
    print request.query.echostr
    return request.query.echostr



@APP.post('/echo/')
#def wechat_test():
#     #print request.forms.keys()[0]
#     xml = ET.fromstring(request.forms.keys()[0])
#     print xml.findtext("Content")

def wechat_post():
     xml = ET.fromstring(request.forms.keys()[0])
     fromUser = xml.findtext("ToUserName")
     toUser = xml.findtext("FromUserName")
     __MsgType = xml.findtext("MsgType")
     __Content = xml.findtext("Content")
     req = []
     key = []
     if "text" == __MsgType:
        req = __Content.split('_')
        if "hi" == req[0]:
            tStamp = time.time()
            content = "欢迎！输入 h 继续"
        elif "h" == req[0]:
            tStamp = time.time()
            content = "借书：b_书名(创造力)_城市.开始时间(x月y日).结束时间(x月y日)；查询：a_书名(创造力)"
            #b+创造力+南京.5月26日.6月1日
            #a+创造力
        elif "a" == req[0]:
            book = str(req[1].encode('UTF-8'))
            tStamp = time.time()
            index = KV.getkeys_by_prefix(book, limit=100, marker=None)
            print index
            #['\xe5\x88\x9b\xe9\x80\xa0\xe5\x8a\x9b1432571672.73']
            con = ""
            for i in index:
               con = con + "%s \n"% KV.get(i)
               print KV.get(i)
               #ovcFVtwLC-7dEArda7gzgfgOPaH0.南京.5月26日.6月1日
            print con
            content = "%s \n %s"% (book.decode('UTF-8'),con)
            #创造力 
            #ovcFVtwLC-7dEArda7gzgfgOPaH0.南京.5月26日.6月1日 
            #ovcFVtwLC-7dEArda7gzgfgOPaH0.南京.5月26日.6月1日
        elif "b" == req[0]:
            key = str(req[1].encode('UTF-8')) + str(time.time())
            print key
            #创造力1432571303.12
            value = toUser + "." + req[2]
            print value
            #ovcFVtwLC-7dEArda7gzgfgOPaH0.南京.5月26日.6月1日
            KV.add(key, value)
            tStamp = time.time()
            content = "%s OK :)"% (req[1] + "." + req[2]) 
            #创造力.南京.5月26日.6月1日
        else :
            tStamp = time.time()
            content = "输入 h 继续使用"
        print CFG.TPL_TEXT% locals()
        return CFG.TPL_TEXT% locals()
     return None

