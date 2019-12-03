# -*- coding: UTF-8 -*-
import os
import datetime
import shutil
from flask import Flask, jsonify, request, render_template, make_response
from flask_cors import CORS
import pdfkit
from utils.files import *
from utils.pdfkits import *

app = Flask(__name__)
CORS(app, supports_credentials=True)

# @app.before_request
# def before_request():
#     current_user = get_jwt_identity()
#     print(current_user)
#     if current_user is None:
#         return jsonify({"error": "JWT authentication is required !!!"}), 401

@app.route('/', methods=[ 'GET', 'POST' ])
def index():
    auth = request.authorization
    print(auth)

    return render_template('index.html')

# curl -v -H "Content-type: application/json" -X POST http://192.168.10.126:8084/pdf
# curl -XPOST -F file=@index.html -F file=@index.css -F file=@style.css http://192.168.10.126:8084/pdf > test.pdf
@app.route('/pdf', methods=[ 'GET', 'POST' ])
def pdf():
    authorization = request.authorization
    # print(authorization)

    # options = {}
    obj = {}
    if request.method == 'POST':
        if request.json is not None:
            if is_json(request.json):
                obj = request.json
        else:
            obj = get_forms(request)

    # obj['flag'] = 'file'
    # # obj['filename'] = 'apache.pdf'
    # # obj['data'] = 'https://www.google.co.jp/'
    # html = {}
    # html['filename'] = 'index.html'
    # html['data'] = 'PCFET0NUWVBFIGh0bWw+CjxodG1sPgogIDxoZWFkPgogICAgPG1ldGEgY2hhcnNldD0idXRmLTgiPgogICAgPHRpdGxlPlNDIEZpbGUgQVBJIHYwLjEuMDwvdGl0bGU+CiAgICA8bGluayByZWw9InN0eWxlc2hlZXQiIHR5cGU9InRleHQvY3NzIiBocmVmPSJpbmRleC5jc3MiPgogICAgPGxpbmsgcmVsPSJzdHlsZXNoZWV0IiB0eXBlPSJ0ZXh0L2NzcyIgaHJlZj0ic3R5bGUuY3NzIj4KICA8L2hlYWQ+Cjxib2R5Pgo8ZGl2IGNsYXNzPSJjYXJkIj4KICAgIEZpbGUgQVBJIOaXpeacrOiqngo8L2Rpdj4KPGRpdiBjbGFzcz0iYm94Ij4KICBGaWxlIEFQSSDml6XmnKzoqp4gMDIKPC9kaXY+CjwvYm9keT4KPC9odG1sPg=='
    # css = {}
    # css['filename'] = 'index.css'
    # css['data'] = 'ZGl2LmJveCB7CiAgICBiYWNrZ3JvdW5kOnJlZDsKICAgIGxpbmUtaGVpZ2h0OjEuNTsKfQ=='
    # css1 = {}
    # css1['filename'] = 'style.css'
    # css1['data'] = 'ZGl2IHsKICAgIGNvbG9yOmJsdWU7CiAgICBsaW5lLWhlaWdodDoxLjU7Cn0='
    # obj['data'] = [ html, css, css1 ]
    result = get_pdf(obj)
    print(result)

    if result is not None:
        response = make_response()
        filename = result['filename']
        fullpath = result['path'] + '/' + filename
        response.data = open(fullpath, 'rb').read()
        response.headers['Content-Disposition'] = "attachment; filename=" + filename
        response.mimetype = 'application/pdf'

        delete_dir(result['path'])
        return response
    else:
        if result is None:
            result = { 'msg': 'Json Data is error !!!' }
        return jsonify(result), 200

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8084)