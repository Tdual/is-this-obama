# -*- coding: utf-8 -*-

from bottle import request
from bottle import Bottle

import json
import os
import sys

sys.path.append(os.getcwd() + '/domain')

from response import put_response
from log import log_debug
from getface import cutout_face, get_face_image_name
from prob import Prob
import filemanager



app = Bottle()
prob = Prob()

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
    files = request.files
    res = filemanager.upload_file(files)
    if res["status"] == "success":
        name = res["detail"]["name"]
        id = res["detail"]["id"]
        save_path = filemanager.get_save_path(id)
        cutout_face(save_path,name,save_path)
    return put_response(res)

@app.route('/images/<image_id>/face', method="GET")
def get_face(image_id):
    fullpath = get_face_image_name(image_id)
    with open(fullpath) as f:
        image = f.read()
        # TODO invalid content_type
    return put_response(image,content_type="image/*")

@app.route('/images/<image_id>/rectangle', method="GET")
def get_face(image_id):
    fullpath = get_face_image_name(image_id,type="rect")
    with open(fullpath) as f:
        image = f.read()
        # TODO invalid content_type
    return put_response(image,content_type="image/*")

@app.route('/images/<image_id>/probability', method="GET")
def get_probability(image_id):
    res = prob.get_prob(image_id)
    return put_response(res)

@app.route('/static/<file_type>/<file>')
def read_static(file_type, file):
    return open('static/'+file_type+'/'+file).read()

if __name__ == '__main__':
    from bottle import run
    app.run(host="0.0.0.0", port=8080)
else:
    log_debug("uwsgi")
    application = app
