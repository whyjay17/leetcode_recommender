import numpy as np
# from nltk.corpus import stopwords

class QuestionMatcher(object):
    """
    A class used to retrieve similar questions using a Word2Vec model.

    Attributes
    ----------
    model : gensim.models.keyedvectors
        a trained word2vec model that will be used to compute question similarity
    
    Methods
    -------
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


    def to_word_vector(self, content):
        content = content.split(' ')
        content_vector = []
        for word in content:
            try:
                # ignore if the word is not in the embeddings
                vector = self.model[word]
                content_vector.append(vector)
            except KeyError:
                pass
        
        res_vector = np.mean(content_vector, axis = 0)
        return res_vector


    def get_similarity(self, q1, q2):
        q1_vec = self.to_word_vector(q1)
        q2_vec = self.to_word_vector(q2)
        # compute cosine similarity
        similarity = np.dot(q1_vec, q2_vec) / (np.linalg.norm(q1_vec) * np.linalg.norm(q2_vec))
        return 0 if np.isnan(np.sum(similarity)) else similarity

    def get_recommendations(self, question, others, threshold = 0):
        
        recommendations = []
        for q in others: # others is a list of tuples (question_name, question_content)
            similarity = self.get_similarity(question, q)
            if similarity > threshold:
                recommendations.append({
                    'name': q[0],
                    'content': q[1],
                    'score': similarity
                })
        recommendations.sort(key = lambda k: k['score'], reverse = True)
        return recommendations

