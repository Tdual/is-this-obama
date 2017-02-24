# -*- coding: utf-8 -*-
import sys
import os
import numpy as np
import tensorflow as tf
import tensorflow.python.platform
import cv2

class CNN(object):
    def __init__(self):
        self.NUM_CLASSES = 2
        self.IMAGE_SIZE = 28
        self.IMAGE_PIXELS = self.IMAGE_SIZE*self.IMAGE_SIZE*3
        self.MAX_STEPS = 200
        self.BATCH_SIZE = 10
        self.LEARNING_RATE = 1e-4
        self.LOG_DIR = '/var/log'

    def inference(self, images_placeholder, keep_prob):
        u"""
        inference

        :param tensorflow.python.framework.ops.Tensor images_placeholder: 画像のplaceholder
        :param tensorflow.python.framework.ops.Tensor keep_prob: dropout率のplace_holder
        :return: softmax
        :rtype: tensorflow.python.framework.ops.Tensor
        """

        def weight_variable(shape):
          u"""
          """
          initial = tf.truncated_normal(shape, stddev=0.1,dtype=tf.float32)
          return tf.Variable(initial,tf.float32)

        def bias_variable(shape):
          u"""
          """
          initial = tf.constant(0.1, shape=shape,dtype=tf.float32)
          return tf.Variable(initial,tf.float32)

        def conv2d(x, W):
          u"""
          """
          return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')

        def max_pool_2x2(x):
          u"""
          """
          return tf.nn.max_pool(x, ksize=[1, 2, 2, 1],
                                strides=[1, 2, 2, 1], padding='SAME')

        x_image = tf.reshape(images_placeholder, [-1, 28, 28, 3])

        with tf.name_scope('conv1') as scope:
            W_conv1 = weight_variable([5, 5, 3, 32])
            b_conv1 = bias_variable([32])
            h_conv1 = tf.nn.relu(conv2d(x_image, W_conv1) + b_conv1)
            
            tf.summary.histogram("W_conv1", W_conv1)
            tf.summary.histogram("b_conv1", b_conv1)
            tf.summary.histogram("h_conv1", h_conv1)

        with tf.name_scope('pool1') as scope:
            h_pool1 = max_pool_2x2(h_conv1)
            
            tf.summary.histogram("h_pool1", h_pool1)

        with tf.name_scope('conv2') as scope:
            W_conv2 = weight_variable([5, 5, 32, 64])
            b_conv2 = bias_variable([64])
            h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2)
            
            tf.summary.histogram("W_conv2", W_conv2)
            tf.summary.histogram("b_conv2", b_conv2)
            tf.summary.histogram("h_conv2", h_conv2)

        with tf.name_scope('pool2') as scope:
            h_pool2 = max_pool_2x2(h_conv2)
            
            tf.summary.histogram("h_pool2", h_pool2)

        with tf.name_scope('fc1') as scope:
            W_fc1 = weight_variable([7*7*64, 1024])
            b_fc1 = bias_variable([1024])
            h_pool2_flat = tf.reshape(h_pool2, [-1, 7*7*64])
            h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)
            
            h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)
            
            tf.summary.histogram("W", W_fc1)
            tf.summary.histogram("b", b_fc1)
            tf.summary.histogram("h", h_fc1)
            tf.summary.histogram("h_drop", h_fc1_drop)
            

        with tf.name_scope('fc2') as scope:
            W_fc2 = weight_variable([1024, self.NUM_CLASSES])
            b_fc2 = bias_variable([self.NUM_CLASSES])
            
            tf.summary.histogram("W_fc2", W_fc2)
            tf.summary.histogram("b_fc2", b_fc2)

        with tf.name_scope('softmax') as scope:
            y_conv=tf.nn.softmax(tf.matmul(h_fc1_drop, W_fc2) + b_fc2)
        return y_conv

    def loss(self, softmax, labels):
        u"""
        loss

        :param softmax: tensor of softmax, float - [batch_size, NUM_CLASSES]
        :param labels: tensor of labels, int32 - [batch_size, NUM_CLASSES]
        :return: cross entropy
        """
        #cross_entropy = -tf.reduce_sum(labels*tf.log(softmax))
        cross_entropy = -tf.reduce_sum(labels*tf.log(tf.clip_by_value(softmax,1.0e-50,1.0)))
        tf.summary.scalar("cross_entropy", cross_entropy)
        return cross_entropy

    def training(self, loss, learning_rate):
        u"""
        training

        :param loss: tensor of loss(result of loss())
        :param learning_rate: learning rate
        :return: Op of training
        """
        train_step = tf.train.AdamOptimizer(learning_rate).minimize(loss)
        return train_step

    def accuracy(self, softmax, labels):
        u"""
        accuracy

        :params softmax: result of inference()
        :params labels: tensor of labels, int32 - [batch_size, NUM_CLASSES]
        :return: rate of correct prediction(float)
        """
        correct_prediction = tf.equal(tf.argmax(softmax, 1), tf.argmax(labels, 1))
        accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))
        tf.summary.scalar("accuracy", accuracy)
        return accuracy

    def read_image(self, data_list, image_size=None):
        """
        data_list = [
            {
            "folder": "name,
            "label" : "0"
            },...
        ]
        """
        if not image_size:
            image_size = self.IMAGE_SIZE
        img_list = []
        label_list = []
        image_name_list = []
        for data in data_list:
            folder = data["folder"]
            label = data["label"]
            for img_name in os.listdir(folder):
                img_path = os.getcwd() + "/"+folder+"/"
                fullpath = img_path + img_name
                image_name_list.append(fullpath)
                jpeg_r = tf.read_file(fullpath)
                image = tf.image.decode_jpeg(jpeg_r)
                resized_img = tf.image.resize_images(image, image_size, image_size)
                reshaped_img = tf.reshape(resized_img,[-1])
                size = image_size * image_size * 3
                reg_matrix = tf.fill([size], 255.0)
                result_img = tf.div(reshaped_img,reg_matrix)
                img_list.append(result_img)
                tmp = np.zeros(2)
                tmp[int(label)] = 1
                label_list.append(tmp)
        return img_list, label_list, image_name_list

    def shape_CVimage(self, CVimage, image_size=None):
        if not image_size:
            image_size = self.IMAGE_SIZE
        resize_img = cv2.resize(CVimage, (image_size, image_size))
        result_img = resize_img.flatten().astype(np.float32)/255.0
        return result_img

    def read_image_cv(self, data_list, image_size=None):
        """
        data_list = [
            {
            "folder": "name,
            "label" : "0"
            },...
        ]
        """
        if not image_size:
            image_size = self.IMAGE_SIZE
        img_list = []
        label_list = []
        image_name_list = []
        for data in data_list:
            folder = data["folder"]
            label = data["label"]
            for i, img_name in enumerate(os.listdir(folder)):
                if not img_name == '.DS_Store':
                    img_path = os.getcwd() + "/"+folder+"/"
                    fullpath = img_path + img_name
                    image_name_list.append(fullpath)
                    img = cv2.imread(fullpath)
                    resize_img = cv2.resize(img, (image_size, image_size))
                    result_img = resize_img.flatten().astype(np.float32)/255.0
                    img_list.append(result_img)
                    tmp = np.zeros(2)
                    tmp[int(label)] = 1
                    label_list.append(tmp)
                if i == 250:
                    break
        return img_list, label_list, image_name_list

    def display_test_prob(self, session, softmax, test_image,
        label_0_name, images_placeholder, keep_prob):
        train_prob = session.run(softmax, feed_dict={
            images_placeholder: test_image,
            keep_prob: 1.0})
        for i, pro in enumerate(train_prob):
            a = "this is " + label_0_name+"！" if pro[0] > 0.8 else "this is not "+label_0_name
            p = pro[0]
            print a + " (rate of "+label_0_name+": "+str(p)+")"
            #display(Image(filename=test_image_list[i]))
