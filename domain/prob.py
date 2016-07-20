# -*- coding: utf-8 -*-
import cv2
import tensorflow as tf
import numpy as np
from cnn import CNN
import os


def get_prob(image_id):
    c = CNN()
    path = os.path.join(os.getcwd(), "var/tmp", image_id)
    image_list = os.listdir(path)
    for img in image_list:
        if "face_" in img:
            image_name = img
            break

    cv_image = cv2.imread(os.path.join(path, image_name))
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
        return prob
