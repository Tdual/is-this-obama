# -*- coding: utf-8 -*-
import cv2
import tensorflow as tf
import numpy as np
from cnn import CNN
import os
import re

from getface import get_face_image_name
from filemanager import get_save_path
from log import log_debug


class Prob(object):
    def __init__(self):
        self.c = CNN()
        self.images_placeholder = tf.placeholder("float")
        self.keep_prob = tf.placeholder("float")
        self.softmax = self.c.inference(self.images_placeholder, self.keep_prob)
        self.saver = tf.train.Saver()

    def get_prob(self, image_id):

        save_path = get_save_path(image_id)
        face_list = [img for img in os.listdir(save_path) if "face_" in img]
        p = {}
        for image_name in face_list:
            _image_num = re.search(r"_\d+_",image_name).group()
            image_num = _image_num[1:][:-1]
            CVimage = cv2.imread(save_path+"/"+image_name)
            image = self.c.shape_CVimage(CVimage)
            with tf.Session() as sess:
                ckpt = tf.train.get_checkpoint_state('./')
                if ckpt: # checkpointがある場合
                    last_model = ckpt.model_checkpoint_path # 最後に保存したmodelへのパス
                    self.saver.restore(sess, last_model) # 変数データの読み込み
                #self.saver.restore(sess, "/root/share/domain/model.ckpt")
                prob = sess.run(self.softmax, feed_dict={
                    self.images_placeholder: [image],
                    self.keep_prob: 1.0
                })[0][0]

            if prob:
                p[image_num] = float(prob)
            else:
                res = {
                    "status":"error",
                    "message":"can not get valid probability",
                }
                return res
        res = {
            "status":"success",
            "data_type": "detail",
            "detail": {"probability": p}
        }
        return res
