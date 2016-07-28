# is-this-obama

## demo site
http://is-this-obama.com/

## description
this web site judges whether a uploded photo is Obama or not. the judge mechanism is the deep learning(CNN).


## development environment

#### deep learning info
language: python   
frame work: tensorflow  
type: CNN  
training data set: obama:120, non obama:120(search for a actor)  

#### web site language
server: python (FM: bottle)  
frontend: JS (FM: React)

#### server environment
nginx + uwsgi



## memo
### data structure between router(app.py) and domain
#### success
```
 {
   "status":"success",
   "data_type": "detail",
   "detail": <detail data: dict>
 }
 ```
 #### error
 ```
 {
   "status:"error",
   "code": <error code: int>
   "http_status": <http status: str>
}
 ```
### example of API response
#### upload success
```
 {
   "id": "afsgsrdgrsdhsrh",
   "name": "test.jpeg"
 }
 ```
 #### error
 ```
 {
   "error": {
     "code": 1
     "message": "can not recognize a face"
   }
}
 ```

### settings
js (react + eslint + webpack )
```
npm install --save react react-dom
npm install -g eslint
eslint --init
npm install --save-dev webpack babel-loader babel-core babel-preset-react babel-preset-es2015

sudo ln -fs /usr/bin/nodejs /usr/local/bin/node
```

```
sudo apt -y update
sudo apt -y upgrade
sudo apt -y install nginx
sudo apt -y install python-pip python-dev
sudo apt -y install wget unzip git
sudo apt -y install npm

sudo pip install --upgrade  https://storage.googleapis.com/tensorflow/linux/cpu/tensorflow-0.8.0-cp27-none-linux_x86_64.whl
sudo pip install uwsgi
sudo pip install bottle

```

cv2
```
sudo apt install -y cmake
sudo apt install -y build-essential
sudo apt install -y python-dev python-numpy libtbb2 libtbb-dev libjpeg-dev libpng-dev libtiff-dev libjasper-dev libdc1394-22-dev
wget https://github.com/Itseez/opencv/archive/3.1.0.zip
unzip 3.1.0.zip
cd opencv-3.1.0
mkdir build
cd build
cmake -D CMAKE_BUILD_TYPE=RELEASE -D VERBOSE=1 -D WITH_GSTREAMER=OFF -D CMAKE_INSTALL_PREFIX=/usr/local ..
make -j $(nproc)
sudo make install
```



```
ssh-keygen
```
save key in github repo

```
sudo service nginx start
```
check browser  

change root to app's path in conf/nginx/sites-enabled/default
```
sudo cp /home/ubuntu/is-this-obama/conf/nginx/sites-enabled/default /etc/nginx/sites-enabled/default


```
change app's path in uwsgi.ini
```
sudo mkdir /var/run/uwsgi/
sudo touch /var/run/uwsgi/app.pid
sudo uwsgi uwsgi.ini
```
