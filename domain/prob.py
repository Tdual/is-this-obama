# -*- coding: utf-8 -*-
import cv2
import tensorflow as tf
import numpy as np
from cnn import CNN
import os

from getface import get_face_image_name
from log import log_debug


def get_prob(image_id):
    c = CNN()

    image_name = get_face_image_name(image_id)
    cv_image = cv2.imread(image_name)
    image = c.shape_CVimage(cv_image)

    images_placeholder = tf.placeholder("float")
    keep_prob = tf.placeholder("float")
    softmax = c.inference(images_placeholder, keep_prob)
    with tf.Session() as sess:
        saver = tf.train.Saver()
        saver.restore(sess, "/root/share/domain/model.ckpt")
        prob = sess.run(softmax, feed_dict={
            images_placeholder: [image],
            keep_prob: 1.0})
    res_prob = prob[0][0]
    data = {
        "status":"success",
        "data_type": "detail",
        "detail": {"probability": float(res_prob)}
    }
    return data
