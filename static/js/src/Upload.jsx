import React from "react";
import FileUpload from 'react-fileupload';


export default class Upload extends React.Component {
  constructor(props) {
    super(props);
    let dataUrl = "";
  }
  render(){
    console.log(window.location.origin);
    const options={
      baseUrl: "http://localhost:8090/upload",
      param:{
        fid:0
      },
      chooseFile(file){
        console.log(file);
        let reader = new FileReader();
        reader.readAsDataURL(file[0]);
        reader.onload = () => {
          this.dataUrl = reader.result;
          console.log(this.dataUrl);
        };
      }
    };
    return (
       <FileUpload options={options}>
           <button ref="chooseBtn">choose</button>
           <button ref="uploadBtn">upload</button>
       </FileUpload>
   );
  }
}
