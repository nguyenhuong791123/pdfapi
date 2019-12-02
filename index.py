# -*- coding: UTF-8 -*-
import os
import datetime
import shutil
from flask import Flask, jsonify, request, render_template, make_response
from flask_cors import CORS
import pdfkit
# from utils.sftp import *

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
@app.route('/pdf', methods=[ 'GET' ])
def pdf():
    authorization = request.authorization
    # print(authorization)

    # options = {}
    if request.method == 'POST':
        if request.json is not None:
            if is_json(request.json):
                auth = request.json.get('auth')

    auth = {}
    auth['flag'] = 'file'
    auth['data'] = 'https://codeday.me/jp/qa/20190916/1591973.html'
    options = {
        'page-size': 'A4',
        'margin-top': '0.1in',
        'margin-right': '0.1in',
        'margin-bottom': '0.1in',
        'margin-left': '0.1in',
        'encoding': "utf-8",
        'no-outline': None,
        'disable-smart-shrinking': '',
    }

    dir = './dowload'
    filename = 'apache.pdf'
    fullpath = dir + '/ '+ 'apache.pdf'
    if auth['flag'] == 'url':
        pdfkit.from_url('https://google.com', fullpath, options=options)
    elif auth['flag'] == 'file':
        pdfkit.from_file('html/index.html', fullpath, css='html/style.css', options=options)
    else:
        pdfkit.from_string('<html><body><h1>It works!</h1></body></html>', fullpath, options=options)

    response = make_response()
    response.data = open(fullpath, 'rb').read()
    response.headers['Content-Disposition'] = "attachment; filename=" + filename
    response.mimetype = 'application/pdf'
    return response

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8084)