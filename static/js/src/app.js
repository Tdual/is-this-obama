import React from "react";
import ReactDOM from "react-dom";
import CommentBox from "./CommentBox";
import Upload from "./Upload"

let handleDrageEnter = (e) => {console.log(e);};

ReactDOM.render(
  <CommentBox url="/test/comments" />,
  document.getElementById("app")
);

ReactDOM.render(
  <Upload />,
  document.getElementById("upload")
);
