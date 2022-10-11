import React , { useReducer} from "react";
import './Base_form.component.css'

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

    const handleSubmit = async (event) => {
        event.preventDefault()
        AppToBase({
            Question : "",
            Answer : ""
        })
        isloading(true)

        const Q_mode = {
            Question : formData.Question,
            Answering_Method : formData.Answering_Method
        }
        let response = await fetch('/answer-question' , {
            method: "POST",
            headers: {
            'Content-Type' : 'application/json'
            }, 
            body: JSON.stringify(Q_mode)
        })
        response = await response.json();
        
        AppToBase({
            Question : formData.Question,
            Answer : response
        })
        isloading(false)
        
        setTimeout(() => {
            setFormData({
                reset: true
            })
            AppToBase({
                Question : null,
                Answer : null
            })
        } , 25000) 
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
            <form onSubmit={handleSubmit}>
                <fieldset className="mb-2 w-75 m-auto pb-3">
                    <label className="form-label text-muted pb-3" htmlFor="QuestionControl" >Question</label>
                    <input name="Question" className="form-control" id="QuestionControl" onChange={handleChange} placeholder="Please Enter Your Question" value={formData.Question || ""} required/>
                </fieldset>
                <fieldset className="mb-4 pb-2">
                    <legend className="form-label title text-muted pb-2">Select Your Method To Calculate</legend>
                    <div className="btn-group shadow-0" role="group">

                        <input type="radio" id="lda" className="btn-check" name="Answering_Method" checked={formData.Answering_Method === "LDA"} onChange={handleChange} value="LDA" required/>
                        <label className="btn btn-outline-dark" htmlFor="lda" >LDA</label>

                        <input className="btn-check" type="radio" id="Sentence_Embedding" name="Answering_Method" checked={formData.Answering_Method === "Sentence_Embedding"} value="Sentence_Embedding" onChange={handleChange} required/>
                        <label className="btn btn-outline-dark" htmlFor="Sentence_Embedding">SentenceEmbedding</label>
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