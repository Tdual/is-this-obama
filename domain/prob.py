# -*- coding: utf-8 -*-
import cv2
import tensorflow as tf
import numpy as np
from cnn import CNN
import os

from getface import get_face_image_name
from filemanager import remove_save_path
from log import log_debug


class Prob(object):
    def __init__(self):
        self.c = CNN()
        self.images_placeholder = tf.placeholder("float")
        self.keep_prob = tf.placeholder("float")
        self.softmax = self.c.inference(self.images_placeholder, self.keep_prob)
        self.saver = tf.train.Saver()

    def get_prob(self, image_id):

        image_name = get_face_image_name(image_id)
        cv_image = cv2.imread(image_name)
        image = self.c.shape_CVimage(cv_image)

        with tf.Session() as sess:
            self.saver.restore(sess, "/root/share/domain/model.ckpt")
            prob = sess.run(self.softmax, feed_dict={
                self.images_placeholder: [image],
                self.keep_prob: 1.0})[0][0]

        if prob:
            res = {
                "status":"success",
                "data_type": "detail",
                "detail": {"probability": float(prob)}
            }
        else:
            res = {
                "status":"error",
                "message":"can not get valid probability",
            }
        return res
