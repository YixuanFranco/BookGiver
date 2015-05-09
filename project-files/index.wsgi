# encoding=utf8
import sae
#导入Bottle模块
from bottle import Bottle,route, run, template, request, response,  post, get, static_file,debug
app=Bottle()
debug(True)  #打开debug功能

@app.get('/')
def web_index():
    return "bookgiver:share books with others"

application = sae.create_wsgi_app(app)
