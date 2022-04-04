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
    """

    def __init__(self, input, input_type="content"):
        """
        overload constructor with a list of strings (content) or with a list of absolute filenames
        but build a consistent Vectorizer of input_type 'content' to handle both cases in search

        :returns: corpus object
        """
        self.nr_documents_loaded = 0  #initialize dictionary

        if input_type == "content":
            texts = input
        else:
            if input_type == "filename":
                texts = self.load_texts(input)
                self.nr_documents_loaded = len(texts)
            else:
                raise SyntaxError("input_type should be 'content' or 'filename'")
        self.documents = input  # required to extract row labels from sparse matrix
        self.vectorizer = HashingVectorizer(input="content",
                                            stop_words=None,  # not filtering out any words > 2 chars
                                            decode_error="ignore",
                                            strip_accents="unicode",
                                            lowercase=True,
                                            n_features=2 ** 18,
                                            alternate_sign=False)
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


