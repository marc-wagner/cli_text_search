"""
unit tests for Corpus class
"""
import numpy as np
from scipy.sparse import csr_matrix

from cli_text_search.corpus import Corpus


class TestCorpus:

    corpus = Corpus(["one one one two three four five"])


    def test_get_document_term_matrix(self):
        assert False


    def test_get_dictionary(self):
        corpus_dict = self.corpus.get_dictionary()
        assert "one" in corpus_dict
        assert "zero" not in corpus_dict
        assert len(corpus_dict) == 5


    def test_get_tokens_in_document(self):
        assert False


    def test_get_best_match(self):
        assert False


    def test_apply_floor_zero(self):

        input_csr = csr_matrix(np.array([0, -1, 1]))
        expected_csr = csr_matrix(np.array([0, 0, 1]))

        result_csr = Corpus.apply_floor_zero(input_csr)

        assert result_csr[0, 1] == expected_csr[0, 1]
        assert result_csr[0, 0] == expected_csr[0, 0]
        assert result_csr[0, 2] == expected_csr[0, 2]
