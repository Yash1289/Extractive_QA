from nltk import FreqDist

def keep_top_k_words(text , top_k_words):
    #Function to only keep those words which are present in top_k_words list
    return [word for word in text if word in top_k_words]

def Df_Processing(df ,min_tokens , k_words):

    '''This function is used to process our dataframe , we first calculate the top k
    words from all the passages and then filtering out the tokenised words which are not present in 
    top k words list'''
    
    #Creating a list of all the tokenised words
    all_words = [word for item in list(df['tokenized']) for word in item]
    fdist = FreqDist(all_words)

    #Finding the words with the most frequency
    k = k_words
    top_k_words = fdist.most_common(k)
    top_k_words,_ = zip(*fdist.most_common(k))
    top_k_words = set(top_k_words)

    #Filtering our tokenised columns to only contain the most frequent words
    df['tokenized'] = df['tokenized'].apply(keep_top_k_words , args = (top_k_words,))

    #Only keeping records which have greater than a specified number of tokens
    df = df[df['tokenized'].map(len) >= min_tokens] 
    df = df[df['tokenized'].map(type) == list]
    df.reset_index(drop=True,inplace=True)

    return df
