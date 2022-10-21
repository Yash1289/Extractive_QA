from ctypes.wintypes import POINT
from re import U
import re
import spacy
import os
import pandas as pd
import numpy as np
from requests import request
import io

from Utils.AnswerExtractor import AnswerExtractor
from Utils.DocumentRetrieval import DocumentRetrieval
from Utils.TextPreProcessing import apply_all
from Utils.QueryPassageProcessing import PassageRetrieval, QueryProcessor
from Utils.PdfExtractor import PdfExtractor
from Utils.DfProcessing import Df_Processing
from Utils.QA_similarity import df_maker , embed_and_sim
from model.lda_model import train_lda


from sentence_transformers import SentenceTransformer
from flask import Flask , request , jsonify, send_from_directory
from flask_cors import CORS , cross_origin
from werkzeug.utils import secure_filename

app = Flask(__name__, static_url_path='', static_folder='EQA_frontend/build')

SPACY_MODEL = os.environ.get('SPACY_MODEL', 'en_core_web_sm')
QA_MODEL = os.environ.get('QA_MODEL', 'distilbert-base-cased-distilled-squad')

nlp = spacy.load(SPACY_MODEL, disable=['ner', 'parser', 'textcat'])
em_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

CORS(app)

query_processor = QueryProcessor(nlp)
document_retriever = DocumentRetrieval()
passages_c = PassageRetrieval()
answer_extractor = AnswerExtractor(QA_MODEL, QA_MODEL)


@app.route("/pdf-upload" , methods = ['POST'])
@cross_origin()
def pUpload():
    if request.method == "POST":
        f = request.files['file_from_react']
        if f and (f.filename).endswith(".pdf"):
            filename = secure_filename(f.filename)
            global file_path
            file_path = os.path.join('temp_files', filename)
            f.save(file_path)
            return { "Status" : "Successfully Uploaded"} , 201
        else:
            return {"Status" : "Error encountered"} , 500
    
    

@app.route('/answer-question' , methods = ['POST'])
@cross_origin()
def eqa():
    data = request.json
    question = data.get('Question')
    answering_method = data.get('Answering_Method')
    usePdf = data.get('usePdf')

    query = query_processor.generate_query(question)
    k_words = 2000
    try:
        if usePdf:
            passages = PdfExtractor(file_path) 
            passages = [ re.sub(r"\n","", passage) for passage in passages]
            os.remove(file_path)
            min_tokens = 15
        elif answering_method == "Sentence_Embedding":
            docs = document_retriever.search(query, 5)
            passages = passages_c.fit(docs)
            min_tokens = 30
        else:
            docs = document_retriever.search(query, 2)
            passages = passages_c.fit(docs)
            min_tokens = 52
            k_words = 800
    

        df = pd.DataFrame(passages ,columns = ["Passage"])
        df['tokenized'] = df['Passage'].apply(apply_all , lemma = True)
        df = Df_Processing(df , min_tokens , k_words)

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
        return jsonify(answer),201
    except:
        return { "status" : "Error encountered"},500
    

@app.route('/')
@cross_origin()
def serve():
    return send_from_directory(app.static_folder , 'index.html')

if __name__ == '__main__':
    app.run()  