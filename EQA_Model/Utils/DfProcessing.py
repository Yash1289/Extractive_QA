from nltk import FreqDist

def keep_top_k_words(text , top_k_words):
    return [word for word in text if word in top_k_words]

def Df_Processing(df):
    
    all_words = [word for item in list(df['tokenized']) for word in item]
    fdist = FreqDist(all_words)

    k = 2500
    top_k_words = fdist.most_common(k)
    top_k_words,_ = zip(*fdist.most_common(k))
    top_k_words = set(top_k_words)

    df['tokenized'] = df['tokenized'].apply(keep_top_k_words , args = (top_k_words,))

    df = df[df['tokenized'].map(len) >= 30]
    # make sure all tokenized items are lists
    df = df[df['tokenized'].map(type) == list]
    df.reset_index(drop=True,inplace=True)

    return df
