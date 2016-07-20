# -*- coding: utf-8 -*-
from bottle import response, HTTPResponse
import json


def put_response(data, status=200, content_type="application/json"):
    if content_type == "image/*":
        data = data
        res = HTTPResponse(body=data, status=status)
        res.set_header('Content-Type', content_type)
        res.set_header('Access-Control-Allow-Origin', '*')
    elif data["status"] == "error":
        if status == 200:
            status = 500
        body = {"error":{"message": data["message"]}}
        res = HTTPResponse(body=body, status=status)
        res.set_header('Content-Type', 'application/json')
        res.set_header('Access-Control-Allow-Origin', '*')
    else:
        if isinstance(data, dict):
            if data["data_type"] == "detail":
                data = json.dumps(data["detail"])
            else:
                data = json.dumps(data["list"])
        else:
            data = {}
        res = HTTPResponse(body=data, status=status)
        res.set_header('Content-Type', content_type)
        res.set_header('Access-Control-Allow-Origin', '*')
    return res
