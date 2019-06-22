import numpy as np

class QuestionMatcher(object):
    """
    A class used to retrieve similar questions using a Word2Vec model.

    Attributes
    ----------
    model : gensim.models.keyedvectors
        a trained word2vec model that will be used to compute question similarity
    
    Methods
    -------
    clean_content(content: str)
        clean up raw question text to remove examples and useless words

    to_word_vector(content: str)
        vectorize the given question content 
    
    get_similarity(q1: np.array, q2: np.array)
        get the cosine similarity between two vectorized question contents
    
    get_recommendations(question: str, threshold: float)
        return all similar questions that exceeds the given threshold value 
        given the question content
    """
    def __init__(self, model):
        self.model = model
    
    def clean_content(self, content):
        pass

    def to_word_vector(self, content):
        pass
    
    def get_similarity(self, q1, q2):
        pass
    
    def get_recommendations(self, question):
        pass