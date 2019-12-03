# -*- coding: UTF-8 -*-
import os
import datetime
import shutil
from flask import Flask, jsonify, request, render_template, make_response
from flask_cors import CORS
import pdfkit
from utils.utils import is_exist
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

    obj = {}
    if request.method == 'POST':
        if request.json is not None:
            if is_json(request.json):
                obj = request.json
        else:
            obj = get_forms(request)

    # options = {}
    # options['orientation'] = 'Portrait'
    # obj['options'] = options
    result = get_pdf(obj)
    if result is not None and is_exist(result, 'msg') == False:
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