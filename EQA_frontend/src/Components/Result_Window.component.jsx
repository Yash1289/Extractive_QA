import React , {useState , useEffect} from "react";
import "./Result_Window.component.css"
import useCollapse from 'react-collapsed'
import RandomFacts from "./random_facts.component";

function ResultWindow({A_found , Q_asked}){

    const [isExpanded, setExpanded] = useState(false)
    const { getCollapseProps, getToggleProps } = useCollapse({ isExpanded })
    const [facts , setfacts] = useState([])

    useEffect(() => {
        const factgen = async () => {
            let response = await fetch('https://api.api-ninjas.com/v1/facts?limit=30' , {
            method: "GET",
            headers: { 'X-Api-Key': '0yW/gLIcVVVtPuhgwXirnw==aEtk73GMQqeE4eZV'},
            contentType: 'application/json'
        })
        response = await response.json(); 
        setfacts(response.sort( ()=>Math.random()-0.5 )) }
        factgen()
    },[])

    useEffect(() => {
        if (!!A_found){
            setExpanded(false)
        }
      }, [A_found]);

    return A_found ? (<div className="R_Wrapper border rounded bg-light p-4">
            <p className="text-center text-muted">
                {Q_asked.split('')
                                    .map((letter, index) =>
                                    index === 0 ? letter.toUpperCase() : letter.toLowerCase(),
                                    )
                                    .join('')}: </p> 
                <strong className="pb-2">{A_found[0]} </strong>
                <div>
                    <button className="btn btn-primary mb-3"
                        {...getToggleProps({
                        onClick: () => setExpanded((prevExpanded) => !prevExpanded),
                        })}
                    >
                        {isExpanded ?'Hide other Answers': 'Show other Answers' }
                    </button>
                    <ul {...getCollapseProps()} className ="list-group">
                        { A_found.slice(1,5).map( (answer , index) => {
                           return( <li key={index} className="list-group-item text-muted li_size">{answer}</li> ) ;
                        })}
                    </ul>
                </div>
        </div>): 
        (<div className="R_Wrapper border rounded bg-light d-flex justify-content-around">
                <span className="d-inline-block mb-3">The answer will show here</span>
                <RandomFacts factArr={facts}></RandomFacts>
        </div>)       
}

export default ResultWindow 