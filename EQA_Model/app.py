from ctypes.wintypes import POINT
from re import U

from requests import request
from Utils.AnswerExtractor import AnswerExtractor
from Utils.DocumentRetrieval import DocumentRetrieval
from Utils.TextPreProcessing import apply_all
from Utils.QueryPassageProcessing import PassageRetrieval, QueryProcessor
from Utils.DfProcessing import Df_Processing
from model.lda_model import train_lda
import spacy
import os
import pandas as pd
import numpy as np
from Utils.QA_similarity import df_maker , embed_and_sim
from sentence_transformers import SentenceTransformer

from flask import Flask , request , jsonify


app = Flask(__name__)
SPACY_MODEL = os.environ.get('SPACY_MODEL', 'en_core_web_sm')
QA_MODEL = os.environ.get('QA_MODEL', 'distilbert-base-cased-distilled-squad')
nlp = spacy.load(SPACY_MODEL, disable=['ner', 'parser', 'textcat'])
em_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')


query_processor = QueryProcessor(nlp)
document_retriever = DocumentRetrieval()
passages_c = PassageRetrieval()
answer_extractor = AnswerExtractor(QA_MODEL, QA_MODEL)

#What is the full name of Obama 565
#name one popular deep learning framework 2530
#what is the value of avogadro's number 2128

@app.route('/')
def index():
    return {
        "sample" : "template"
    }

@app.route('/answer-question' , methods = ['POST'])
def eqa():
    data = request.json
    question = data.get('Question')
    answering_method = data.get('Answering_Method')

    query = query_processor.generate_query(question)

    if answering_method == "Sentence_Embedding":
        docs = document_retriever.search(query, -1)
    else:
        docs = document_retriever.search(query, 3)

    passages = passages_c.fit(docs)
    print(len(passages))

    df = pd.DataFrame(passages ,columns = ["Passage"])
    df['tokenized'] = df['Passage'].apply(apply_all , lemma = True)
    df = Df_Processing(df)

    if answering_method == "Sentence_Embedding":

        passages_and_q = list(df["Passage"].values)
        passages_and_q.append(question)
        passages = embed_and_sim(em_model , passages_and_q)
    else:

        dictionary,corpus,lda = train_lda(df)
        doc_topic_dist = np.array([[tup[1] for tup in lst] for lst in lda[corpus]])
        passages = df_maker(em_model ,df , lda, question , doc_topic_dist )

    answers = answer_extractor.extract(question, passages)
    answer = [answer["answer"] for answer in answers]
    return jsonify(answer)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)