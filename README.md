# is-this-obama

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

### setting js (react + eslint + webpack )
```
npm install --save react react-dom
npm install -g eslint
eslint --init
npm install --save-dev webpack babel-loader babel-core babel-preset-react babel-preset-es2015
```
