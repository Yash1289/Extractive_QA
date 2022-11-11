#Importing all the necessary libraries
import os
import spacy
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from flask import jsonify
import re


#Importing all the custom modules
from Utils.AnswerExtractor import AnswerExtractor
from Utils.DocumentRetrieval import DocumentRetrieval
from Utils.TextPreProcessing import apply_all
from Utils.QueryPassageProcessing import PassageRetrieval, QueryProcessor
from Utils.PdfExtractor import PdfExtractor
from Utils.DfProcessing import Df_Processing
from Utils.QA_similarity import df_maker , embed_and_sim
from model.lda_model import train_lda

#Retriving the necessary models from environment variables
SPACY_MODEL = os.environ.get('SPACY_MODEL', 'en_core_web_sm')
QA_MODEL = os.environ.get('QA_MODEL', 'distilbert-base-cased-distilled-squad')

nlp = spacy.load(SPACY_MODEL, disable=['ner', 'parser', 'textcat'])
em_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

#Creating instances of all the different imported class 
query_processor = QueryProcessor(nlp)
document_retriever = DocumentRetrieval()
passages_c = PassageRetrieval()
answer_extractor = AnswerExtractor(QA_MODEL, QA_MODEL)
 

def GetAnswers(usePdf, answering_method , question ,file_path = None):

        '''This function receives the question , answering method and file path as arguments
        and using all this information it generates answers relevant to the question asked'''

        #Retreiving the query tokens from the question asked
        query = query_processor.generate_query(question)
        k_words = 2000

        #Creating a list of passages depending on the anwering method choosed
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
    
        #Creating one pandas dataframe to store the passages 
        df = pd.DataFrame(passages ,columns = ["Passage"])
        df['tokenized'] = df['Passage'].apply(apply_all , lemma = True)
        df = Df_Processing(df , min_tokens , k_words)

        #Finding the top passages depeding on the answering method choosed
        if answering_method == "Sentence_Embedding":

            passages_and_q = list(df["Passage"].values)
            passages_and_q.append(question)
            passages = embed_and_sim(em_model , passages_and_q)
        else:

            _ ,corpus,lda = train_lda(df)
            doc_topic_dist = np.array([[tup[1] for tup in lst] for lst in lda[corpus]])
            passages = df_maker(em_model ,df , lda, question , doc_topic_dist )

        #Extracting possible answers from the top n passages 
        answers = answer_extractor.extract(question, passages)
        
        answer = [answer["answer"] for answer in answers]
        return jsonify(answer)