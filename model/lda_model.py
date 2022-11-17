import gensim
from gensim.models import LdaModel
from gensim import models, corpora, similarities

def train_lda(data):
    """
    This function trains the lda model
    We setup parameters like number of topics, the chunksize to fix the number of document processed at a time
    We also do 4 passes of the data since this is a small dataset, so we want the distributions to stabilize
    """
    num_topics = 8

    chunksize = 50
    #Creating a dictionary representation of the documents
    dictionary = corpora.Dictionary(data['tokenized'])
    # Bag-of-words representation of the documents.
    corpus = [dictionary.doc2bow(doc) for doc in data['tokenized']]

    lda = LdaModel(corpus=corpus, num_topics=num_topics, id2word=dictionary,
                   alpha=0.9e-2, eta=0.5e-2, chunksize=chunksize, minimum_probability=0.0, passes=4 , random_state = 1)
    return dictionary,corpus,lda