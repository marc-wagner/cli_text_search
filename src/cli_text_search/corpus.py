import os

from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
import numpy as np

import document

class Corpus:

    df_dtm = pd.DataFrame()

    def __init__(self, document_paths):
        # TODO check what attributes are really worth persisting in object model
        self.documents = document_paths
        self.vectorizer = CountVectorizer(input="filename")  # not using any stop_words : not filtering out any words > 2 chars
        self.n_gram_matrix = self.vectorizer.fit_transform(self.documents)

        # TODO make scaleable with this:
        # https://scikit-learn.org/stable/auto_examples/applications/plot_out_of_core_classification.html#sphx-glr-auto-examples-applications-plot-out-of-core-classification-py


    def get_document_term_matrix(self):
        return pd.DataFrame(data=self.n_gram_matrix.toarray(),
                            # TODO check type and simplify
                            index=pd.DataFrame({'document_path': self.document_paths}).values,
                            columns=self.vectorizer.get_feature_names_out())

    def get_best_match(self, search_term, max_rank=1):

        # TODO rewrite this to use a clean string.
        # try:
        #     temp_file = open("../../tmp/search_term.txt", "w")
        #     temp_file.write(search_term)
        #     temp_file.close()
        #
        #     vectorized_search_term = self.vectorizer.transform(list("../../tmp/search_term.txt")).toarray()
        # except FileNotFoundError:
        #     raise("could not write to temporary file tmp/search_term")

        score = []
        for i in range(1 , len(self.documents)):
            score.append((i,np.linalg.norm(self.n_gram_matrix[i+1, :], self.n_gram_matrix[i, :])))


        score.sort(lambda x : x[2])
        return score[1 : max_rank]
