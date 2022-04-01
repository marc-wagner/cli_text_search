"""
unit tests for Corpus class
"""
import numpy as np
import pandas
import pytest
from scipy.sparse import csr_matrix

from cli_text_search.corpus import Corpus


class TestCorpus:

    search = "one one one two three four five"
    corpus = Corpus([search])

    def test_constructor_input_type(self):
        with pytest.raises(SyntaxError):
            Corpus([self.search], input_type="invalid")

    def test_get_document_term_matrix_isdf(self):
        result = self.corpus.get_document_term_matrix()
        assert isinstance(result, pandas.core.frame.DataFrame)

    def test_get_document_term_matrix_shape(self):
        result = self.corpus.get_document_term_matrix()
        assert result.to_string() == """                                 five  four  one  three  two
one one one two three four five     1     1    3      1    1"""

    def test_get_dictionary_in(self):
        corpus_dict = self.corpus.get_dictionary()
        assert "one" in corpus_dict

    def test_get_dictionary_not_in(self):
        corpus_dict = self.corpus.get_dictionary()
        assert "zero" not in corpus_dict
        assert len(corpus_dict) == 5

    def test_get_dictionary_len(self):
        corpus_dict = self.corpus.get_dictionary()
        assert len(corpus_dict) == 5

    def test_get_tokens_in_document_max(self):
        assert False

    def test_get_tokens_in_document_min(self):
        assert False

    def test_get_best_match_sort_desc(self):
        # elements are sorted desc
        assert False

    def test_get_best_match_no_match(self):
        # return empty array
        assert False

    def test_get_best_match_max(self):
        # max nr tokens found < nr tokens
        assert False

    def test_apply_floor_zero(self):

        input_csr = csr_matrix(np.array([0, -1, 1]))
        expected_csr = csr_matrix(np.array([0, 0, 1])).toarray()
        result_csr = Corpus.apply_floor_zero(input_csr)
        assert str(result_csr) == str(expected_csr)