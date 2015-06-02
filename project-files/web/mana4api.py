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
#key = 书名+openid
#value = 南京.5月26日.6月1日

bk = sae.kvdb.KVClient()
#key = book+time()
#value = 书名

##############
lk = sae.kvdb.KVClient()
#key = openid
#value = 微信号

wx = sae.kvdb.KVClient()
#key = [num]
#value = 微信号

r = "注册微信号：r_微信号"

w = "获取指定借阅请求的微信号：w_序号"


##############
b = "借书：b_书名(创造力)_城市.开始时间(x月y日).结束时间(x月y日)"
a = "查询所有书目：a"
m = "查看某个书目的所有借阅请求：m_书名(创造力)"
s = "查看自己提交的请求：s"
d = "删除请求：d_书名(创造力)"


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
#     req = []

#     index = []
#     key = ""
#     value = ""
#     bk_index = []
#     bk_key = ""
#     bk_value = ""
#     lk_key = ""
#     lk_value = ""
#     book = ""
     con = ""

     if "text" == __MsgType:
        req = __Content.split('_')
        if "hi" == req[0] or "HI" == req[0] or "Hi" == req[0]:
            content = "欢迎！输入 h 继续"

        elif "h" == req[0] or "H" == req[0]:
            content = "%s \n%s \n%s \n%s \n%s \n%s \n%s"% (r,b,a,m,w,s,d)
            #b+创造力+南京.5月26日.6月1日
            #a+创造力

        elif "a" == req[0] or "A" == req[0] :
            bk_index = bk.getkeys_by_prefix("book", limit=100, marker=None)
            for i in bk_index:
               con = con + "\n %s"% bk.get(i)
            content = "all books %s"% con

        elif "m" == req[0] or "M" == req[0] :
            book = str(req[1].encode('UTF-8'))
            index = KV.getkeys_by_prefix(book, limit=100, marker=None)
            key_spl = []
            n = 0
            for i in index:
               key_spl = i.split('+')
               wechat = lk.get(key_spl[1])
               
               wx.set(str(n), wechat, min_compress_len=0)

               con += "\n %s %s.%s"% (str(n),wechat ,KV.get(i))
               
               n += 1

               #ovcFVtwLC-7dEArda7gzgfgOPaH0.南京.5月26日.6月1日

            content = "%s %s"% (book.decode('UTF-8'),con)
            #创造力 
            #ovcFVtwLC-7dEArda7gzgfgOPaH0.南京.5月26日.6月1日 
            #ovcFVtwLC-7dEArda7gzgfgOPaH0.南京.5月26日.6月1日


        elif "b" == req[0] or "B" == req[0]:
            book = str(req[1].encode('UTF-8'))
            #创造力

            key = book + "+" + toUser
            #创造力+ovcFVtwLC-7dEArda7gzgfgOPaH0
            value = req[2]
            #南京.5月26日.6月1日
            KV.add(key, value)

            content = "%s OK :)"% (book.decode('UTF-8') + "." + req[2]) 
            #创造力.南京.5月26日.6月1日


            #保存书目的数据库，用于查询所有需要借阅的书籍信息
            bk_key = "book" + str(time.time())
            bk_value = str(req[1].encode('UTF-8'))
            true = 0
            bk_index = bk.getkeys_by_prefix("book", limit=100, marker=None)
            for i in bk_index:
               if bk.get(i) == bk_value :
                  true = 1
            if true == 0:
               bk.add(bk_key , bk_value)

        elif "s" == req[0] or "S" == req[0]:
            bk_index = bk.getkeys_by_prefix("book", limit=100, marker=None)

            for i in bk_index:
               key = bk.get(i) + "+" + toUser
               if KV.get(key) != None :
                  con = con + ("%s.%s \n"% ((bk.get(i)).decode('UTF-8'),KV.get(key)))

            content = "%s "% con
        
        elif "d" == req[0] or "D" == req[0]:
            book = str(req[1].encode('UTF-8'))
            key = book + "+" + toUser
            print key
            KV.delete(key)

            index = KV.getkeys_by_prefix(book, limit=100, marker=None)
            count = 0
            for i in index :
               count += 1
            if count == 0 :  #查找是否还有本书的借阅请求，如果没有
               bk_index = bk.getkeys_by_prefix("book", limit=100, marker=None)
               print bk_index
               for j in bk_index:
                  print j
                  print bk.get(j)
                  if bk.get(j) == book :                                   #查找书目里是否还有该书，如果有
                    bk.delete(j)

            content = "%s deleted"% book.decode('UTF-8')
###
        elif "r" == req[0] or "R" == req[0]:
            lk_key = toUser
            lk_value = req[1]
            n = 2
            if len(req) > 2:
              while n < len(req):
                 lk_value = lk_value + "_" + req[n]
                 n += 1
            lk.set(lk_key,lk_value,min_compress_len=0)
            content = "%s ok"% lk_value

        elif "w" == req[0] or "W" == req[0]:
            weixin = wx.get(req[1])
            content = "%s"% (weixin)
###
        else :
            content = "输入 h 继续使用"

        tStamp = time.time()
        print CFG.TPL_TEXT% locals()
        return CFG.TPL_TEXT% locals()
     return None


