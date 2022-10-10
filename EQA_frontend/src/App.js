import logo from './logo.svg';
import './App.css';
import BaseForm from './Components/Base_form.component';
import ResultWindow from './Components/Result_Window.component';
import React , { useState } from "react";
import LoadingOverlay from 'react-loading-overlay'

function App() {

  const [question , setQuestion ] = useState()
  const [answer , setAnswer ] = useState()
  const [loading , setLoading] = useState()

  const setValues = (data) => {

    console.log(data.Question , data.Answer)
    setQuestion(data.Question)
    setAnswer(data.Answer)

    console.log("from app.js" , answer , question)
  }

  const loadingState = (condition) => {
    setLoading(condition)
  }

  return (
    <div className="App">
      <header className="App-header">
      <LoadingOverlay
          active={loading}
          spinner
          text='Searching for answer...'
          >
            <BaseForm  AppToBase={setValues} isloading = {loadingState}></BaseForm>
      </LoadingOverlay>  
        <ResultWindow A_found = {answer} Q_asked = {question}></ResultWindow>
      </header>
    </div>
  );
}

export default App;
