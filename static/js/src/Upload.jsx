import React from "react";
import Dropzone from 'react-dropzone';
import request from "superagent";

export default class Upload extends React.Component {
  constructor(props){
    super(props);
    this.apiHost = window.location.origin;
    this.state = {
      dataUrl: "",
      prob: "",
      isObama: false,
      errorMessage: ""
    };
  }

  callbackUpload(err, data){
    let res = data.body;
    if(err) {
      let error = data.body.error;
      this.setState({
        //dataUrl:"",
        errorMessage: error.message
      });
    }else{
      let id = res.id;
      if(id){
        this.getProb(id);
      }
    }
  }

  callbackGetProb(err, data){
    let probs  = data.body.probability;
    let max = 0;
    let maxKey = 0;
    let pKeys = Object.keys(probs);
    for (let k in pKeys){
      if(max < probs[k]){
        max = probs[k];
        maxKey = k;
      }
    }
    this.changeImage(maxKey);
    let prob = max;
    let isObama = prob > 0.9;
    this.setState({prob,isObama});
  }

  changeImage(maxKey){
    let url = `${this.state.dataUrl}/indiviual/${maxKey}`;
    this.setState({ dataUrl: url });
  }

  getProb(id){
    let baseUrl = `/images/${id}`;
    let rectUrl = `${baseUrl}/rectangle`;
    let probUrl = `${baseUrl}/probability`;
    this.setState({dataUrl: rectUrl});
    let req = request.get(probUrl);
    req.end(this.callbackGetProb.bind(this));
  }

  onDrop(files) {
    this.setState({
      errorMessage:"",
      prob: 0
    });
    let file = files[0];
    var reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => {
      this.setState({ dataUrl: reader.result });
    };
    let uploadUrl = "/upload";
    let req = request.post(uploadUrl);
    req.attach(file.name, file);
    req.end(this.callbackUpload.bind(this));
  }

  render() {
    return (
          <div>
            <Dropzone
              onDrop={this.onDrop.bind(this)}
              accept="image/gif, image/jpeg,image/png,image/jpg"
              multiple = {false}
            >
              <div>drop some files here, or click to select file to upload.</div>
            </Dropzone>
           <span className={this.state.prob && !this.state.errorMessage? "show":"hidden"}>
             This is {this.state.isObama? "":"not " } Obama! (Obama's face rate: {this.state.prob*100} %)
           </span>
           <span className={this.state.errorMessage? "errorMessage show":"hidden"}>
             {this.state.errorMessage}
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
