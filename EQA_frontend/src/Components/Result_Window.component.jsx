import React from "react";
import "./Result_Window.component.css"

function ResultWindow({A_found , Q_asked}){

    console.log("from result window " , A_found)

    return A_found ? (<div className="R_Wrapper border rounded bg-light p-4">
            <p className="text-center text-muted">
                {Q_asked.split('')
                                    .map((letter, index) =>
                                    index === 0 ? letter.toUpperCase() : letter.toLowerCase(),
                                    )
                                    .join('')}: </p> 
                <br/> 
                <strong className="pb-2">{A_found[0]} </strong>
                <button class="btn btn-primary" type="button" data-bs-toggle="collapse" data-bs-target="#otherAnswers" aria-expanded="false" aria-controls="collapseExample">
                    Show other 4 answers
                </button>
                <ul class="list-group collapse" id="otherAnswers">
                    <strong>hello</strong>
                    { A_found.slice(1,5).forEach(answer => {
                        <li class="list-group-item">{answer}</li>
                    })}
                </ul>

        </div>): (<div className="R_Wrapper border rounded bg-light">The answer will show here </div>)
        
}

export default ResultWindow 