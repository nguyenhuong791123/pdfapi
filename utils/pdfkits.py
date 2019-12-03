# -*- coding: UTF-8 -*-
import os
import pdfkit
from .utils import *
from .dates import *

def get_pdf(obj):
    options = default_options(obj)
    if is_exist(obj, 'data') == False or is_empty(obj['data']):
        return None

    flag = None
    if is_exist(obj, 'flag') and is_empty(obj['flag']) == False:
        flag = obj['flag']

    path = 'download/'
    pattern = get_pattern(True, True, None, True)
    dir = get_datetime(pattern, -3)
    outdir = path + dir
    if os.path.isdir(outdir) == False:
        os.mkdir(outdir)

    filename = dir + '_sc.pdf'
    if is_exist(obj, 'filename') and is_empty(obj['filename']) == False:
        filename = obj['filename']

    result = {}
    try:
        outpath = os.path.join(outdir, filename)
        data = obj['data']
        if flag == 'url':
            print(data)
            print(outpath)
            print(os.getcwd())
            pdfkit.from_url(data, outpath, options=options)
        elif flag == 'file':
            if (is_exist(data, 'html') == False) or is_empty(data['html']['data']):
                return None

            htmlname = data['html']['filename']
            html = os.path.join(outdir, htmlname)
            convert_b64_string_to_file(data['html']['data'], html)
            css = None
            if is_exist(data, 'css') and is_empty(data['css']['data']) == False:
                cssname = data['css']['filename']
                css = os.path.join(outdir, cssname)
                convert_b64_string_to_file(data['css']['data'], css)

            if css is None:
                pdfkit.from_file(html, outpath, options=options)
            else:
                pdfkit.from_file(html, outpath, css=css, options=options)
        else:
            pdfkit.from_string(data, outpath, options=options)
    except IOError as e:
        result['msg'] = str(e)
    finally:
        result['path'] = outdir
        result['filename'] = filename

    return result

def default_options(obj):
    opts = {
        'page-size': 'A4',
        'orientation': 'Portrait', #'Landscape'
        'margin-top': '0.1in',
        'margin-right': '0.1in',
        'margin-bottom': '0.1in',
        'margin-left': '0.1in',
        'encoding': "utf-8",
        'no-outline': None,
        'disable-smart-shrinking': ''
    }
    if is_exist(obj, 'options') == False or is_json(obj['options']) == False:
        return opts

    options = obj['options']
    for key in options.keys():
        if is_empty(options[key]):
            continue
        opts[key] = options[key]

    return opts