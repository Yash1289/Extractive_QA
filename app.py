#Importing libraries
from ctypes.wintypes import POINT
from re import U
import os
from requests import request
import io
from flask import Flask , request , send_from_directory
from flask_cors import CORS , cross_origin
from werkzeug.utils import secure_filename

from answers.get_answers import GetAnswers

#Initializing our app 
app = Flask(__name__, static_url_path='', static_folder='EQA_frontend/build')


#Initialzing the CORS extension with our app
CORS(app)


#Creating one post route to upload pdf files
@app.route("/pdf-upload" , methods = ['POST'])
@cross_origin()
def pUpload():
    if request.method == "POST":
        #storing the uploaded pdf file on backend
        f = request.files['file_from_react']
        if f and (f.filename).endswith(".pdf"):
            filename = secure_filename(f.filename)
            global file_path
            file_path = os.path.join('temp_files', filename)
            f.save(file_path)
            return { "Status" : "Successfully Uploaded"} , 201
        else:
            return {"Status" : "Error encountered"} , 500
    
    
#Creating one post route to get the question and answers from the frontend
@app.route('/answer-question' , methods = ['POST'])
@cross_origin()
def eqa():
    data = request.json

    #storing all the data received from frontend into variables
    question = data.get('Question')
    answering_method = data.get('Answering_Method')
    usePdf = data.get('usePdf')

    try:
        if usePdf:
            answer = GetAnswers(usePdf , answering_method , question, file_path)
        else:
            answer = GetAnswers(usePdf , answering_method , question)
        return answer,201
    except Exception as e:
        print(e)
        return { "status" : "Error encountered"},500
    

@app.route('/')
@cross_origin()
def serve():
    return send_from_directory(app.static_folder , 'index.html')

if __name__ == '__main__':
    app.run()  