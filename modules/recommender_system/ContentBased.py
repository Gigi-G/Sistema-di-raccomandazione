import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from stop_words import get_stop_words
import numpy as np

class ContentBased():

    def __init__(self, subjects_filename, data_filename = None, data = None, threshold = 0.22) -> None:
        self.threshold = threshold
        self.__build_tfidf_matrix(subjects_filename)
        if(data_filename is not None):
            self.__build_utility_matrix(data_filename)
        elif(data is not None):
            self.data = data
            self.utility_matrix = data
        else:
            print("Error in data initialization!")
            exit(-1)
        self.__build_normalized_utility_matrix()
        self.__build_user_profiles()

    def __build_tfidf_matrix(self, subjects_filename) -> None:
        ds = pd.read_csv(subjects_filename)
        tf = TfidfVectorizer(stop_words = get_stop_words("italian"))
        self.tfidf_matrix = tf.fit_transform([(k.split(" - ")[1]) for k in ds['description']])
        self.tfidf_matrix = np.where(np.array(self.tfidf_matrix.todense()) > self.threshold, 1, 0)
    
    def __build_utility_matrix(self, data_filename) -> None:
        self.data = pd.read_csv(data_filename)
        self.utility_matrix = self.data.pivot_table(index='user_id', columns='subject_id', values='rating')

    def __build_normalized_utility_matrix(self) -> None:
        self.n_utility_matrix = self.utility_matrix.sub(self.utility_matrix.mean(1), axis = 'index').fillna(0).to_numpy()
    
    def __build_user_profiles(self) -> None:
        self.profiles = []
        for user in self.n_utility_matrix:
            profile = []
            for item in self.tfidf_matrix.transpose():
                profile.append((np.sum(user * item) + 1)/(np.count_nonzero(user) + 1))
            self.profiles.append(profile)
        return np.array(self.profiles)
    
    def __scale(self, X, x_min, x_max):
        nom = (X + 1) * (x_max - x_min)
        denom = 2
        return x_min + nom / denom

    def __cosine_distance(self, x, y) -> float:
        return (np.dot(x, y) + 1) / ((np.sqrt(np.dot(x, x)) + 1) * np.sqrt(np.dot(y, y) + 1))

    def print_utility_matrix(self):
        print(self.utility_matrix)

    def predict(self, xi, sj) -> float:
        return self.__scale(self.__cosine_distance(self.profiles[xi], self.tfidf_matrix[sj]), 0, 5)
