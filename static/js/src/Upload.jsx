import React from "react";
import FileUpload from 'react-fileupload';
import request from "superagent";


export default class Upload extends React.Component {
  constructor(props) {
    super(props);
    this.apiHost = window.location.origin;
    this.state = {
      dataUrl: "",
      faceUrl: "",
      prob: "",
      isObama: false
    };
  }

  handleChooseFile(file){
    let reader = new FileReader();
    reader.readAsDataURL(file[0]);
    reader.onload = () => {
      this.setState({dataUrl: reader.result})
    };

  }

  handleUploadSuccess(res){
    console.log(res);
    let id = res.id;
    if(id){
      let baseUrl = `${this.apiHost}/images/${id}`;
      let rectUrl = `${baseUrl}/rectangle`;
      let probUrl = `${baseUrl}/probability`;
      this.setState({dataUrl: rectUrl});
      request.get(probUrl)
        .end((err, res) => {
          if (err) {
            throw err;
          }
          console.log(res.body);
          let prob = res.body.probability;
          let isObama = prob > 0.9;
          this.setState({prob,isObama});
        });
    }
  }

  render(){
    const options={
      baseUrl: `${this.apiHost}/upload`,
      chooseFile: this.handleChooseFile.bind(this),
      uploadSuccess: this.handleUploadSuccess.bind(this)
    };
    return (
       <FileUpload options={options} dataUrl={this.dataUrl}>
           <button ref="chooseBtn">choose a photo</button>
           <button className={this.state.dataUrl ? "show" : "hidden"} ref="uploadBtn">upload a photo</button>
           <span className={this.state.prob? "show":"hidden"}>
             This is {this.state.isObama? "":"not " } Obama!
           </span>
           <div>
           <span className={this.state.dataUrl ? "show" : "hidden"}>
             <img src={this.state.dataUrl} alt="choosed image" />
           </span>
           </div>
       </FileUpload>
   );
  }
}
