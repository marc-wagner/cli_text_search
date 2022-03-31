import os

from IPython.core.display_functions import display
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
import numpy as np
import logging


class Corpus:

    def __init__(self, document_paths):

        self.documents = document_paths  # required to extract row labels from sparse matrix
        self.vectorizer = CountVectorizer()  # not using any stop_words : not filtering out any words > 2 chars
        self.n_gram_matrix = self.vectorizer.fit_transform(self.load_texts(document_paths))  # requires all documents in memory
        # TODO make scale out with this:
        # https://scikit-learn.org/stable/auto_examples/applications/plot_out_of_core_classification.html#sphx-glr-auto-examples-applications-plot-out-of-core-classification-py

        logging.info(f"corpus document term matrix shape: {self.get_document_term_matrix().shape}")
        logging.debug(f"corpus dictionary: {self.get_dictionary()}")

    def get_document_term_matrix(self):
        """ view matrix in human readable form with
        row headers = document path and column headers = words in document"""
        return pd.DataFrame(data=self.n_gram_matrix.toarray(),
                            index=np.array(self.documents),
                            columns=self.vectorizer.get_feature_names_out())

    def get_dictionary(self):
        """ return dictionary of corpus """
        return self.vectorizer.get_feature_names_out()

    def get_best_match(self, search_term, max_rank=1):

        logging.info(f"searching best match for {search_term} in {len(self.documents)} documents")
        score = []
        input_search_term = [search_term]  # instantiate empty list of strings
        search_term_ngram = self.vectorizer.transform(input_search_term)
        # TODO debug why ceil_1 fails when floor_0 works OK
        # norm_search_term_ngram = self.apply_ceil_ones(search_term_ngram)
        norm_search_term_ngram = search_term_ngram

        target = norm_search_term_ngram.toarray().sum()

        logging.debug(f"built ngram for '{search_term}' : {target} tokens in {type(search_term_ngram)}")

        for i in range(0, len(self.documents)):
            diff_negatives = norm_search_term_ngram - self.n_gram_matrix[i, :]

            diff_coverage = self.apply_floor_zero(diff_negatives)

            logging.debug(f"diff coverage array: {diff_coverage} of type {type(diff_coverage)}")
            sum_coverage = 1-diff_coverage.sum()/target
            if sum_coverage > 0:
                score.append([sum_coverage, self.documents[i]])
            #   score.append((i, np.linalg.norm( search_term_ngram, self.n_gram_matrix[i, :])))
            if len(score) == max_rank:
                break
        score.sort(key=lambda x: x[0], reverse=True)
        nr_results = min(max_rank, len(score))
        logging.info(f"returning {nr_results} best matches")
        return score[0: nr_results]

    @staticmethod
    def apply_floor_zero(diff_negatives):
        zero_array = np.zeros(diff_negatives.shape, dtype=diff_negatives.dtype)
        diff_coverage = np.maximum(diff_negatives.toarray(), zero_array)
        return diff_coverage

    @staticmethod
    def apply_ceil_ones(matrix):
        """remove duplicate words
        required in order to score more accurately"""
        ones_array = np.ones(matrix.shape, dtype=matrix.dtype)
        # TODO debug why ceil_1 fails when floor_0 works OK
        ceil_matrix = np.minimum(matrix, ones_array)
        return ceil_matrix

    @staticmethod
    def load_texts(document_paths):
        texts = []
        # TODO find best way to read fault tolerant
        for path in document_paths:
            try:
                text_file = open(path, "r")
                texts.append(text_file.read())
            finally:
                text_file.close()
        return texts
