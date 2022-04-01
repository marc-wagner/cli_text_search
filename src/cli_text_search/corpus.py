import os

from IPython.core.display_functions import display
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
import numpy as np
import logging


class Corpus:
    """
    a corpus is a collection of documents
    that can be searched for word occurrences
    or via a dictionary

    the class uses scikit learn to vectorize text as bag-of-words n-gram with n=1 and does not use stop words.
    this means that 1-letter words like "I", "a" or abbreviated words like "'s" are ignored for scoring

    The score of a document for a search is determined by its coverage:
    if all search words are present, the score is is a good match for the The score that is returned
    """

    def __init__(self, input, input_type="string"):
        """
        constructor ban be overloaded with a list of strings or with a list of filepaths
        """
        if input_type == "string":
            texts = input
        else:
            if input_type == "filepath":
                texts = self.load_texts(input)
            else:
                raise SyntaxError("input_type should be 'string' or 'filepath'")
        self.documents = input  # required to extract row labels from sparse matrix
        self.vectorizer = CountVectorizer()  # not using any stop_words : not filtering out any words > 2 chars
        self.n_gram_matrix = self.vectorizer.fit_transform(texts)  # requires all documents in memory
        # TODO make scale out with this:
        # https://scikit-learn.org/stable/auto_examples/applications/plot_out_of_core_classification.html#sphx-glr-auto-examples-applications-plot-out-of-core-classification-py

        logging.debug(f"document term matrix shape: {self.get_document_term_matrix().shape}, "
                      f"dictionary: {self.get_dictionary()}")

    def get_document_term_matrix(self):
        """
        view matrix in human readable form with
        row headers = document path and column headers = words in document
        """
        return pd.DataFrame(data=self.n_gram_matrix.toarray(),
                            index=np.array(self.documents),
                            columns=self.vectorizer.get_feature_names_out())

    def get_dictionary(self):
        """
        return dictionary of corpus
        """
        return self.vectorizer.get_feature_names_out()

    def get_tokens_in_document(self, search_ngram, document_index):
        """
        return the number of tokens that were found in document
        initial_token_count = search words that exist in dictionary of ALL documents (<= word count in search )
        """
        initial_token_count = search_ngram.sum()
        diff_negatives = search_ngram - self.n_gram_matrix[document_index, :]
        tokens_not_found = self.apply_floor_zero(diff_negatives)
        return initial_token_count - tokens_not_found.sum()

    def get_best_match(self, search_term, max_rank=1):
        """
        search for string in loaded all documents
        params:
        search_term: a sentence to be separated into words
        max_rank: number of documents to return
        """
        logging.debug(f"searching for '{search_term}' in :{len(self.documents)} documents")
        score = []
        input_search_term = [search_term]  # instantiate empty list of strings
        search_term_ngram = self.vectorizer.transform(input_search_term)  #vectorize against CORPUS dictionary

        if search_term_ngram.sum() == 0:  #no part of the search term is in the corpus
            return score

        for i in range(0, len(self.documents)):  # search in each document's dictionary

            nr_tokens_found = self.get_tokens_in_document(search_term_ngram, i)
            logging.debug(f"found {nr_tokens_found} token(s) in {self.documents[i]}")

            if nr_tokens_found > 0:
                score.append([nr_tokens_found, self.documents[i]])

        score.sort(key=lambda x: x[0], reverse=True)
        nr_results = min(max_rank, len(score))
        logging.debug(f"returning {nr_results} best matches")
        return score[0: nr_results]

    @staticmethod
    def apply_floor_zero(matrix):
        """
        whether a word shows up once or many times in a document doesn't matter,
        the score stays the same
        """
        zero_array = np.zeros(matrix.shape, dtype=matrix.dtype)
        floored_matrix = np.maximum(matrix.toarray(), zero_array)
        return floored_matrix

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
