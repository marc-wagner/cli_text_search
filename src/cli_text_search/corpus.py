import os

from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd

import document

class Corpus:

    df_dtm = pd.DataFrame()

    def __init__(self, document_paths):
        self.documents = document_paths
        texts = []
        for path in document_paths:
            try:
                text_file = open(path, "r")
                texts.append(text_file.read())
            finally:
                text_file.close()

        columns = ['document_path', 'text']
        # df = pd.DataFrame({'document_path': document_paths, 'text': texts})
        df = pd.DataFrame({'document_path': document_paths})

        cv = CountVectorizer(input="filename",stop_words='english')
        # cv_matrix = cv.fit_transform(df['text'])
        cv_matrix = cv.fit_transform(df['document_path'])

        # create document term matrix
        self.df_dtm = pd.DataFrame(data=cv_matrix.toarray(),
                              index=df['document_path'].values,
                              columns=cv.get_feature_names_out())

    def get_best_match(self, word, max_rank=1):
        return 1
