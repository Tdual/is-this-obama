# -*- coding: utf-8 -*-

from bottle import request, response, static_file
from bottle import Bottle

from response import put_response
from log import log_debug
import json

app = Bottle()

@app.route('/test')
def test():
    return "test!\n"

@app.route('/test/json')
def test_json():
    data = {
        "status":"success",
        "data_type": "detail",
        "detail":{
          "message":"test!",
        }
    }
    return put_response(data)

@app.route('/')
def index_html():
    return open('static/html/index.html').read()

if __name__ == '__main__':
    from bottle import run
    app.run(host="0.0.0.0", port=8080)
else:
    log_debug("uwsgi")
    application = app
