import React from "react";
import FileUpload from 'react-fileupload';


export default class Upload extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      dataUrl: ""
    };
  }

  handleChooseFile(file){
    let reader = new FileReader();
    reader.readAsDataURL(file[0]);
    reader.onload = () => {
      this.setState({dataUrl: reader.result})
    };

  }

  render(){
    var host = window.location.origin;
    const options={
      baseUrl: `${host}/upload`,
      param:{
        fid:0
      },
      chooseFile: this.handleChooseFile.bind(this)
    };
    return (
       <FileUpload options={options} dataUrl={this.dataUrl}>
           <button ref="chooseBtn">choose</button>
           <button ref="uploadBtn">upload</button>
           <div>
           <img src={this.state.dataUrl} alt="aaa" />
           </div>
       </FileUpload>
   );
  }
}
