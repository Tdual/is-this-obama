import React from "react";
import Dropzone from 'react-dropzone';
import request from "superagent";

export default class Upload extends React.Component {
  constructor(props){
    super(props);
    this.apiHost = window.location.origin;
    this.state = {
      dataUrl: "",
      faceUrl: "",
      prob: "",
      isObama: false
    };
  }

  callbackUploadSuccess(data){
    let res = data.body;
    let id = res.id;
    if(id){
      this.getProb(id);
    }
  }

  callbackGetProbSuccess(data){
    let prob = data.body.probability;
    let isObama = prob > 0.9;
    this.setState({prob,isObama});
  }

  getProb(id){
    let baseUrl = `/images/${id}`;
    let rectUrl = `${baseUrl}/rectangle`;
    let probUrl = `${baseUrl}/probability`;
    this.setState({dataUrl: rectUrl});
    let req = request.get(probUrl);
    req.then(this.callbackGetProbSuccess.bind(this));
  }

  onDrop(files) {
    let file = files[0];
    let uploadUrl = "/upload";
    let req = request.post(uploadUrl);
    req.attach(file.name, file);
    req.then(this.callbackUploadSuccess.bind(this));
  }

  render() {
    return (
          <div>
            <Dropzone
              onDrop={this.onDrop.bind(this)}
              accept="image/gif,image/jpeg,image/png,image/jpg"
              multiple = {false}
            >
              <div>drop some files here, or click to select file to upload.</div>
            </Dropzone>
           <span className={this.state.prob? "show":"hidden"}>
             This is {this.state.isObama? "":"not " } Obama!(Obama's face rate: {this.state.prob*100} %)
           </span>
           <div>
           <span className={this.state.dataUrl ? "show" : "hidden"}>
             <img src={this.state.dataUrl} alt="choosed image" />
           </span>
           </div>
          </div>
      );
  }
}
