import React from "react";
import "./Pdf_upload.component.css"

function PdfUpload({forwFile, showUpload }) {

  const uploadFile = async (e) => {
    const file = e.target.files[0];
    if (file != null) {
      const data = new FormData();
      data.append('file_from_react', file);
      forwFile(data)
    }
  };

  return (
      <input
        className={`fileU mb-2 ${ showUpload ? `showU` : `hideU`}`}
        type="file"
        required = {showUpload}
        accept=".pdf"
        onClick ={(event)=> { 
          event.target.value = null
     }}
        onChange={uploadFile}>
      </input>
  ) 
}

export default PdfUpload
