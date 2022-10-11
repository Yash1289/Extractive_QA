import itertools

class QueryProcessor:

    def __init__(self, nlp, keep=None):
        self.nlp = nlp
        self.keep = keep or {'PROPN', 'NUM', 'VERB', 'NOUN', 'ADJ'}

    def generate_query(self, text):
        doc = self.nlp(text)
        query = ' '.join(token.text for token in doc if token.pos_ in self.keep)
        return query


class PassageRetrieval:

  def __init__(self):
        self.tokenize = None

  def preprocess(self, doc):
        passages = [p for p in doc.split('\n') if p and not p.startswith('=')]
        return passages
  
  def fit(self, docs):
        passages = list(itertools.chain(*map(self.preprocess, docs)))
        return passages