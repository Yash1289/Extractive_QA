
![Logo](https://i.ibb.co/58gPjTD/logo512.png)


# Automated Question Answering System

In recent years, question answering has emerged as one of the most
popular application of nlp . Most of the companies today relies on one
such chat bot to automatically answer the most common kind of questions asked by the
customer and this enables them to run a 24/7 help and support service. A similar 
kind of system can also be used in the field of education where it can be used
to answer questions from a research paper or from a digital book in the form of
pdf given as context . In this project we are trying to build a hybrid open cum closed domain
question answering system where one can ask questions without providing any context or
they can also upload a document of there liking as context and ask question related to it. 


## Run Locally

Clone the project

```bash
  git clone https://github.com/Yash1289/Extractive_QA.git
```

Go to the project directory

```bash
  cd Extractive_QA-main
```

Install backend dependencies

```bash
  pip install 
```
Start the backend server

```bash
  flask run
```
Go to the frontend directory

```bash
  cd EQA_frontend
```

Install frontend dependencies

```bash
  npm install
```

Start the frontend server

```bash
  npm run start
```


## Code

To retrieve the possible list of 
answers from the given list of context we are using [DistilBERT model](https://huggingface.co/distilbert-base-cased-distilled-squad). DistilBERT is a small, fast, cheap and light Transformer model trained by distilling BERT base.
Originally BERT stands Bidirectional Encoder Representations from Transformers. It is one of the most popular and widely used NLP models. 
BERT models can consider the full context of a word by looking at the words that come before and after it,
which is particularly useful for understanding the intent behind the query asked. The one we are using is trained on [Stanford Question Answering Dataset (SQuAD)](https://huggingface.co/datasets/squad).

For open domain question answering , we are fetching wikipedia articles using the [Wikipedia Api](https://en.wikipedia.org/w/api.php) based on the question
entered by the user and then pre processing them a bit to get chunks of different passages. 

For closed domain question answering in which user will supply the context , we first extract the text
out from the pdf uploaded by the user and then perform a little pre processing to get a list of passages out from it.

To filter out these passages so to remove the ones which are not so relevant to the question , or in 
simple words to find document and question similarity we are using 
two alternative separate methods 

* **Latent Dirichlet Allocation** : Using [LDA](https://radimrehurek.com/gensim/models/ldamodel.html) we first find out the list of topics from the total number of passages given and then we keep only a total number of 10 passages whose topic is most similar to the one asked in question
* **Sentence Embedding** : In this method using a [Sentence Transformer model](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) we map both our question & paragraphs to a 384 dimensional dense vector space and then using cosine similarity we filter out 10 of the most similar passages to the question

And these passages are then passed into our DistilBERT model to get the best possible answer.
## Screenshots

![App Screenshot](https://i.ibb.co/ZGR9ZCZ/p-better-ss.png)
![App Screenshot](https://i.ibb.co/DgQNjpC/pytorch-ans-ss.png)



## Demo

### Here is a working demo of the app `Answer Me!`

![App Demo](https://i.ibb.co/PY1XdY2/Answer-Me-and-23-more-pages-Pers.gif)


## Tech Stack

**Client:** Javascript, React, Bootstrap, CSS

**Server:** Python, flask 


## Authors

- [@Yash1289](https://github.com/Yash1289)


## 🚀 About Me

I'm an aspriring data scientist who loves to `deeply` work with data


## 🔗 Links

[![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/shaurabh-pandey-69484921a/)


