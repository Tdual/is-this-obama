# -*- coding: utf-8 -*-
import cv2
import os
from filemanager import get_save_path

def cutout_face(image_path, image_name, dist_path, rectangle=True):
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
        if rectangle:
            color = (255, 255, 255)
            for rect in facerect:
                cv2.rectangle(image, tuple(rect[0:2]),
                        tuple(rect[0:2] + rect[2:4]), color, thickness=2)
            new_rect_path = dist_path + '/' +'rect_' + image_name;
            cv2.imwrite(new_rect_path, image)

def get_face_image_name(image_id, type="face"):
    u"""

    return: fullpath name
    """
    prefix = type + "_"
    path = get_save_path(image_id)
    if path:
        image_list = os.listdir(path)
        for img in image_list:
            if prefix in img:
                name = img
                break
        return os.path.join(path,name)
    else:
        return None
