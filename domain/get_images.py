# -*- coding: utf8 -*-

import requests
import re
import sys
from bs4 import BeautifulSoup
from PIL import Image
from StringIO import StringIO
import random
import os
import json


def get_images_sync(q):
    url = 'http://www.bing.com/images/search?q='+q
    res = requests.get(url)
    html = res.text
    soup = BeautifulSoup(html, "html.parser")
    img_tags = soup.find_all("img", src=re.compile(r'http://tse\d.mm.bing.net*'))
    for i, t in enumerate(img_tags):
        src_html = t.attrs["src"]
        img = requests.get(src_html)
        j = Image.open(StringIO(img.content)) 
        j.save("/Users/dir/Workspace/nlp/img"+str(i)+".jpeg")
    
    return len(img_tags)

def get_image_async(q, first, folder):
    url = 'http://www.bing.com/images/async?q='+q+'&async=content&first='+str(first)+'&IID=images.1'
    res = requests.get(url)
    html = res.text
    soup = BeautifulSoup(html, "html.parser")
    img_tags = soup.find_all("a")
    total = 0
    for a in img_tags:
        m =  a.get("mad")
        if m:
            m_json = json.loads(m)
            image_url = m_json.get("turl")
            print image_url
            img = requests.get(image_url)
            if img.content:
                j = Image.open(StringIO(img.content)) 
                j.save(folder + "/img"+str(total+first)+".jpeg")
                total = total + 1

    return total 



if __name__ == '__main__':
    #total = get_images_sync()
    #print total

    params = sys.argv
    if len(params) == 1: 
        print "require query word and total."
    elif len(params) == 2:
        print "require total."
    elif len(params) == 3:
        q = params[1]
        req_total = int(params[2])
        first = 0
        folder = os.getcwd() + "/image"
        print("folder's path:{}".format(folder))

        total = first
        while total < req_total:
            total += get_image_async(q, total, folder)
            print total

        print "end"
    else:
        print "invalid params." 
    
    


	
