from nltk.corpus import stopwords 
from nltk import word_tokenize
import re
from textblob import TextBlob
from nltk.stem.porter import PorterStemmer

def initial_clean(text):
    '''
    Function to clean text of websites, email addresess and any punctuation
    We also lower case the text
    '''
    text = re.sub("((\S+)?(http(s)?)(\S+))|((\S+)?(www)(\S+))|((\S+)?(\@)(\S+)?)", " ", text)
    text = re.sub("[^a-zA-Z ]", "", text)
    text = text.lower() # lower case the text
    text = word_tokenize(text)
    return text

stop_words = stopwords.words('english')
def remove_stop_words(text):
    '''
    Function that removes all stopwords from text
    '''
    return " ".join([word for word in text if word not in stop_words])

stemmer = PorterStemmer()
    
def text_normalization(sentence , lemma = None):
    
    if lemma:
      '''Function that will lemmatize the words with its part of speech tag'''

      sent = TextBlob(sentence)
      tag_dict = {"J": 'a', 
                  "N": 'n', 
                  "V": 'v', 
                  "R": 'r'}
      words_and_tags = [(w, tag_dict.get(pos[0], 'n')) for w, pos in sent.tags]    
      lemmatized_list = [wd.lemmatize(tag) for wd, tag in words_and_tags]
      return lemmatized_list
    else :
      try:
        sentence = sentence.split(" ")
        text = [stemmer.stem(word) for word in sentence]
        text = [word for word in text if len(word) > 1] # make sure we have no 1 letter words
      except IndexError: 
        pass
      return text


def apply_all(text , lemma = None):
    '''
    Function to combine the results of different functions
    '''
    return text_normalization(remove_stop_words(initial_clean(text)) , lemma)
 
