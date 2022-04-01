from sklearn.feature_extraction.text import HashingVectorizer
import pandas as pd
import numpy as np
import logging
from corpus import Corpus


class DistributedCorpus(Corpus):
    """Threadsafe version of Corpus class.
    uses sciKit learn HashingVectorizer
    https://scikit-learn.org/stable/auto_examples/applications/plot_out_of_core_classification.html#sphx-glr-auto-examples-applications-plot-out-of-core-classification-py

    Methods:
        __init__(self, input, input_type="content")
        get_document_term_matrix(self)
        get_tokens_in_document(self, search_ngram, document_index)
        get_matching_documents(self, search_term)
        apply_floor_zero(matrix)
    """

    def __init__(self, input, input_type="content"):
        """
        overload constructor with a list of strings (content) or with a list of absolute filenames
        but build a consistent Vectorizer of input_type 'content' to handle both cases in search
        """
        self.nr_documents_loaded = 0  #initialize dictionary

        if input_type == "content":
            texts = input
        else:
            if input_type == "filename":
                texts = self.load_texts(input)
            else:
                raise SyntaxError("input_type should be 'content' or 'filename'")
        self.documents = input  # required to extract row labels from sparse matrix
        self.vectorizer = HashingVectorizer(input="content",
                                          stop_words=None,  # not filtering out any words > 2 chars
                                          decode_error="ignore",
                                          strip_accents="unicode",
                                          lowercase=True)
        self.n_gram_matrix = self.vectorizer.fit_transform(texts)  # requires all documents in memory


        logging.debug(f"document term matrix shape: {self.get_document_term_matrix().shape}")

    def get_document_term_matrix(self):
        """view matrix that matches hash_buckets to documents
        row headers = documents
        column headers = hash buckets
        data = occurrences of hashed term in 'document'

        returns: pandas.dataFrame
        """
        return pd.DataFrame(data=self.n_gram_matrix.toarray(),
                            index=np.array(self.documents))

    def get_dictionary(self):
        """does not exist for hashed corpus
        rType:
        """
        raise AttributeError(f"cannot implement parent function {type(super)}:get_dictionary() in {type(self)}")

    def get_tokens_in_document(self, search_ngram, document_index):
        """Given a search n-gram and the index of a document in corpus count the occurences of each item document.
        Note that initial_token_count = search words that exist in dictionary of ALL documents (<= word count in search)

        :param search_ngram: tokenized search
        :param document_index: index of document in corpus
        :returns initial_token_count - tokens_not_found.sum(): the number of tokens that were found in document
        """
        initial_token_count = search_ngram.sum()
        diff_negatives = search_ngram - self.n_gram_matrix[document_index, :]
        tokens_not_found = self.apply_floor_zero(diff_negatives)
        return initial_token_count - tokens_not_found.sum()

    def get_matching_documents(self, search_term):
        """search for string in all loaded documents

        :param search_term: search string as words separated by whitespace
        :returns score: collection of (nr of tokens found, document file path)
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
        logging.debug(f"returning {len(score)} matches")
        return score

    @staticmethod
    def apply_floor_zero(matrix):
        """apply a floor of zero to all negative values in a matrix
        whether a word shows up once or many times in a document doesn't matter, the score stays the same

        :param matrix: a class that can be cast to a matrix
        :returns floored_matrix: matrix of same type as input, without negative values
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
