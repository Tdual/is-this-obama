# -*- coding: utf-8 -*-
import cv2
import os

def cutout_face(image_path, image_name, dist_path):
    image = cv2.imread(image_path+"/"+image_name)
    cascade_path = '/usr/local/share/OpenCV/haarcascades/haarcascade_frontalface_alt.xml'
    cascade = cv2.CascadeClassifier(cascade_path)
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    facerect = cascade.detectMultiScale(image_gray, scaleFactor=1.2, minNeighbors=2, minSize=(10, 10))
    print "face rectangle(x,y,w,h)"+str(facerect)

    if len(facerect) > 0:
        for i,rect in enumerate(facerect):
            x = rect[0]
            y = rect[1]
            width = rect[2]
            height = rect[3]
            dst = image[y:y+height, x:x+width]
            new_image_path = dist_path + '/' + 'face_'+ image_name;
            cv2.imwrite(new_image_path, dst)
