
# -*- coding: utf-8 -*-

import os
import shutil
import hashlib

from getface import cutout_face

def upload_file(files):
    id = ""
    for name, file in files.items():
        f = file.file.read()
        id = hashlib.md5(f).hexdigest()
        save_path = os.path.join(os.getcwd(), "var/tmp", id)
        if os.path.isdir(save_path):
            shutil.rmtree(save_path)
        os.mkdir(save_path)
        file.file.seek(0)
        file.save(save_path)
        cutout_face(save_path,name,save_path)
    data = {
        "status":"success",
        "data_type": "detail",
        "detail": {"id": id}
    }
    return data
