from tkinter import EW
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd


def topic_list(lda , question):

    '''
    Function to create a string of all the words present in a specific topic 
    and append all such strings one by one into a list
    '''

    topics = []
    for idx, topic_tup in lda.show_topics(formatted = False):
        topics.append([topic_word[0] for topic_word in topic_tup])
    new_sent = list(map(lambda x : " ".join(x) , topics))
    new_sent.append(question)
    return new_sent
    


def df_maker(sen_model, df , lda , question , doc_topic_dist):

    """
    Function to calculate the top 10 passages which are most 
    similar to the question 
    """
    topicQ_strings = topic_list(lda , question)
    sentence_embeddings = sen_model.encode(topicQ_strings)
    sim_arr  = cosine_similarity(
        [sentence_embeddings[-1]],
        sentence_embeddings[:-1]
        )
    mi_topic = np.argsort(sim_arr).flatten()[::-1][:1]
    topicV_df = pd.DataFrame(doc_topic_dist[: , mi_topic] , columns = ["Value"])
    top_n = np.array(topicV_df.sort_values(by = "Value" , ascending = False).index)[:10]
    passages = df["Passage"].values[top_n]
    
    return passages

def embed_and_sim(model , passages):

    '''
    Function to create passages and question embedding so to
     return the top 10 passages similar to the question
    '''

    sentence_embeddings = model.encode(passages)
    sim_arr  = cosine_similarity(
        [sentence_embeddings[-1]],
        sentence_embeddings[:-1]
        )
    sim_arr = sim_arr.flatten()
    top_10_indices = np.argsort(sim_arr)[::-1][:10]
    return np.array(passages)[top_10_indices]