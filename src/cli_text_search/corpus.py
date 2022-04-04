from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
import numpy as np
import logging


class Corpus:
    """
    Corpus is a collection of documents that can be searched for word occurrences or via a dictionary
    the class uses scikit learn to vectorize text as bag-of-words n-gram with n=1 and does not use stop words.
    this means that 1-letter words like "I", "a" or abbreviated words like "'s" are ignored for scoring

    The score of a document for a search is determined by its coverage:
    if all search words are present, the score is is a good match for the The score that is returned

    Methods:
        __init__(self, input, input_type="content")
        get_document_term_matrix(self)
        get_tokens_in_document(self, search_ngram, document_index)
        get_matching_documents(self, search_term)
        apply_floor_zero(matrix)
    """

    def __init__(self, data, input_type="content"):
        """
        overload constructor with a list of strings (content) or with a list of absolute filenames
        but build a consistent Vectorizer of input_type 'content' to handle both cases in search

        :returns: corpus object
        """
        if input_type == "content":
            texts = data
        else:
            if input_type == "filename":
                texts = self.load_texts(data)
            else:
                raise SyntaxError("input_type should be 'content' or 'filename'")
        self.documents = data  # required to extract row labels from sparse matrix
        self.vectorizer = CountVectorizer(input="content",
                                          stop_words=None,  # not filtering out any words > 2 chars
                                          decode_error="ignore",
                                          strip_accents="unicode",
                                          lowercase=True)
        self.n_gram_matrix = self.vectorizer.fit_transform(texts)  # requires all documents in memory
        # TODO make scale out with this:
        # https://scikit-learn.org/stable/auto_examples/applications/plot_out_of_core_classification.html#sphx-glr-auto-examples-applications-plot-out-of-core-classification-py

        logging.debug(f"document term matrix shape: {self.get_document_term_matrix().shape}, "
                      f"dictionary: {self.get_dictionary()}")

    def get_document_term_matrix(self):
        """view matrix that matches terms to documents in human readable form
        row headers = documents
        column headers = terms (words)
        data = occurrences of 'term' in 'document'

        :returns: pandas.dataFrame
        """
        return pd.DataFrame(data=self.n_gram_matrix.toarray(),
                            index=np.array(self.documents),
                            columns=self.vectorizer.get_feature_names_out())

    def get_dictionary(self):
        """
        :returns: the dictionary of corpus
        """
        return self.vectorizer.get_feature_names_out()

    def get_tokens_in_document(self, search_ngram, document_index):
        """Given a search n-gram and the index of a document in corpus count the occurences of each item document.
        Note that initial_token_count = search words that exist in dictionary of ALL documents (<= word count in search)

        :param search_ngram: tokenized search
        :param document_index: index of document in corpus
        :returns: initial_token_count - tokens_not_found.sum(): the number of tokens that were found in document
        """
        initial_token_count = search_ngram.sum()
        diff_negatives = search_ngram - self.n_gram_matrix[document_index, :]
        tokens_not_found = self.apply_floor_zero(diff_negatives)
        return initial_token_count - tokens_not_found.sum()

    def get_matching_documents(self, search_term):
        """search for string in all loaded documents

        :param search_term: search string as words separated by whitespace
        :returns: score: collection of (nr of tokens found, document file path)
        """
        logging.debug(f"searching for '{search_term}' in :{len(self.documents)} documents")
        score = []
        input_search_term = [search_term]  # instantiate empty list of strings
        search_term_ngram = self.vectorizer.transform(input_search_term)  # vectorize against CORPUS dictionary

        if search_term_ngram.sum() == 0:  # no part of the search term is in the corpus
            return score

        for i in range(0, len(self.documents)):  # search in each document's dictionary

            nr_tokens_found = self.get_tokens_in_document(search_term_ngram, i)
            logging.debug(f"found {nr_tokens_found} token(s) in {self.documents[i]}")

            if nr_tokens_found > 0:
                score.append({'score': nr_tokens_found, 'document': self.documents[i]})

        score.sort(key=lambda x: x['score'], reverse=True)
        logging.debug(f"returning {len(score)} matches")
        return score

    @staticmethod
    def apply_floor_zero(matrix):
        """
        Given a matrix, return a matrix with all negative values replaced with zero

        :param matrix: a class that can be cast to a matrix
        :return: A matrix with all negative values set to zero.
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
