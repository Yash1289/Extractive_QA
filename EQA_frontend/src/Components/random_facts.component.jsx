import React , {useEffect , useState , useRef} from "react";
import "./random_facts.component.css"

const RandomFacts = ({factArr}) => {

    const [ fact , setFact ] = useState("To make one pound of whole milk cheese, 10 pounds of whole milk is needed")
    const [fadeProp, setFadeProp] = useState({
        fade: 'fade-in',
    })

    const count = useRef(0);
    
    useEffect(() => {
        const timeout = setInterval(() => {
            if (fadeProp.fade === 'fade-in') {
                setFadeProp({
                    fade: 'fade-out'
                })
            } else {
                setFact(factArr[count.current].fact)
                count.current = (count.current + 1)%30
                setFadeProp({
                    fade: 'fade-in'
                })
            }
        }, 6000);

        return () => clearInterval(timeout)
    }, [fadeProp, factArr])

    return (
        <div className="Fact_box" >
            <p className= {fadeProp.fade} ><em className="text-muted Fact">{fact}</em></p>
        </div>
    )
}

export default RandomFacts