import React , { useReducer, useState} from "react";
import './Base_form.component.css'
import PdfUpload from "./Pdf_upload.component";


const formReducer = (state , event) => {
    if (event.reset){
        return {
            Question : "",
            Answering_Method : ""
        }
    }
    return {
        ...state,
        [event.name] : event.value
    }
} 

function BaseForm({AppToBase , isloading }) {

    const [formData , setFormData ] = useReducer(formReducer , {} )
    const [ usePdf ,setPdf ] = useState(false)
    const [ file , setfile ] = useState("")

    const handleFile = (fileData) => {
        setfile(fileData)
    }

    const handleSubmit = async (event) => {
        event.preventDefault()
        window.clearTimeout(timeoutHandling)
        AppToBase({
            Question : "",
            Answer : ""
        })
        isloading(true)

        const Q_mode = {
            Question : formData.Question,
            Answering_Method : formData.Answering_Method,
            usePdf : usePdf
        }

        if (usePdf && file){
            let responsef = await fetch('/pdf-upload',
            { 
            method: 'post',
            body: file,
            }
        );
            let res = await responsef.json();
            if (responsef.status !== 201){
                alert('Error uploading file');
                isloading(false)
            }
        }
        
        let response = await fetch('/answer-question' , {
            method: "POST",
            headers: {
            'Content-Type' : 'application/json'
            }, 
            body: JSON.stringify(Q_mode)
        })
        let response_result = await response.json();
        if (response.status !== 201){
            alert('Error uploading file');
            isloading(false)
        } 

        AppToBase({
            Question : formData.Question,
            Answer : response_result
        })
        isloading(false)
        setFormData({
            reset: true
        })
        var timeoutHandling = setTimeout(() => {
            AppToBase({
                Question : "",
                Answer : ""
            })
        },15000)
        // Need to figure out how to keep audience engaged like if we don't reset apptobase thing, then some issues
    }

    const triggertoggle =() =>{
        setPdf(!usePdf)
        if (!usePdf){
            setfile("")
        }
    }

    const handleChange = event => {


       setFormData({
            name : event.target.name,
            value : event.target.value,
        });
    }

    var position

    const changePosition = (e) => {
        if (!formData.Question || (!formData.Answering_Method)){
            position ? (position = 0) : (position = 100);
            e.target.style.transform = `translate(${position}px, 0px)`;
            e.target.style.transform = "all 0.3s ease";
        }
        else {
           position = 0
            e.target.style.transform = `translate(${position}px, 0px)`;
            e.target.style.transform = "all 0.3s ease"; 
            return
        }
    }

    return (
        <div className="Wrapper border rounded bg-light p-3">
            <h2 className="mb-5 Banner">ANSWER ME!</h2>
            <form className="sizer" onSubmit={handleSubmit}>
                <fieldset className="mb-1 w-75 m-auto pb-3">
                    <label className="form-label text-muted pb-3" htmlFor="QuestionControl" >Question</label>
                    <input name="Question" className="form-control" id="QuestionControl" onChange={handleChange} placeholder="Please Enter Your Question" value={formData.Question || ""} required/>
                </fieldset>
                <PdfUpload forwFile={handleFile} showUpload={usePdf}></PdfUpload>
                <fieldset className= "mb-4 pb-2">
                    <legend className="form-label title text-muted pb-2">Select Your Method To Calculate</legend>
                    <div className="d-flex justify-content-center">
                        <div className="btn-group shadow-0 me-4 method" role="group">
                            <input type="radio" id="lda" className="btn-check" name="Answering_Method" checked={formData.Answering_Method === "LDA"} onChange={handleChange} value="LDA" required/>
                            <label className="btn btn-outline-dark" htmlFor="lda" >LDA</label>

                            <input className="btn-check" type="radio" id="Sentence_Embedding" name="Answering_Method" checked={formData.Answering_Method === "Sentence_Embedding"} value="Sentence_Embedding" onChange={handleChange} required/>
                            <label className="btn btn-outline-dark" htmlFor="Sentence_Embedding">SentenceEmbedding</label>
                        </div>
			            <div className="form-check form-switch">
                            <input className="form-check-input" type="checkbox" role="switch" id="flexSwitchCheckDefault" checked={usePdf} onChange={triggertoggle}/>
                            <label className="form-check-label" htmlFor="flexSwitchCheckDefault">Pdf</label>
                        </div>
                    </div>
                </fieldset>
                
                <div className="d-flex justify-content-evenly mb-3">
                    <button onMouseOver={changePosition} className="btn btn-success" type="submit" >Submit</button>
                </div>  
            </form>
        </div>
    )
}

export default BaseForm