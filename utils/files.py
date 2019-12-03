# -*- coding: UTF-8 -*-
import os
from .dates import *

def save_files(files, outdir):
    if os.path.isdir(outdir) == False:
        os.mkdir(outdir)

    result = []
    for file in files:
        if file is None:
            continue

        f = {}
        f['filename'] = file.filename
        f['data'] = outdir
        file.save(os.path.join(outdir, file.filename))
        result.append(f)

    return result

def get_dir(dir):
    pattern = get_pattern(True, True, None, True)
    outdir = get_datetime(pattern, -3)
    if dir is None:
        return outdir
    else:
        return os.path.join(dir, outdir)

def get_ext(filename):
    if filename is None:
        return None
    return filename.split(".")[-1]
