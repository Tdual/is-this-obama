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

@app.route('/test/comments', method="POST")
def test_json():
    req = request.json
    log_debug("########")
    log_debug(req)
    log_debug("########")
    data = {
        "status":"success",
        "data_type": "detail",
        "detail": req
    }
    return put_response(data)

@app.route('/')
def index_html():
    return open('static/html/index.html').read()

@app.route('/upload', method="POST")
def upload_file():
    log_debug("$$$$$$$$$$$$$$$$$")

@app.route('/static/<file_type>/<file>')
def read_static(file_type, file):
    return open('static/'+file_type+'/'+file).read()

if __name__ == '__main__':
    from bottle import run
    app.run(host="0.0.0.0", port=8080)
else:
    log_debug("uwsgi")
    application = app
