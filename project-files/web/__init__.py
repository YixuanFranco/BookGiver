# -*- coding: utf-8 -*-
from bottle import *

APP = Bottle()
APP.mount('/api', __import__('mana4api').APP)

@APP.error(404)
def error404(error):
    return template('404.html')

@APP.route('/favicon.ico')
def favicon():
    abort(204)

