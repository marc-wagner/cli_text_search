"""
unit tests for Corpus class
"""
import numpy as np
import pandas
import pytest
from scipy.sparse import csr_matrix

from cli_text_search.corpus import Corpus


class TestCorpus:

    content = "one one one two three four five"
    multi_content = ["one one one two three four five", "one two three four"]
    search = "four five six"
    corpus_singleton = Corpus([content])
    corpus_multiple = Corpus(multi_content)

    def test_constructor_input_type(self):
        with pytest.raises(SyntaxError):
            Corpus([self.content], input_type="invalid")

    def test_get_document_term_matrix_isdf(self):
        result = self.corpus_singleton.get_document_term_matrix()
        assert isinstance(result, pandas.core.frame.DataFrame)

    def test_get_document_term_matrix_shape(self):
        result = self.corpus_singleton.get_document_term_matrix()
        assert result.to_string() == """                                 five  four  one  three  two
one one one two three four five     1     1    3      1    1"""

    def test_get_dictionary_in(self):
        corpus_dict = self.corpus_singleton.get_dictionary()
        assert "one" in corpus_dict

    def test_get_dictionary_not_in(self):
        corpus_dict = self.corpus_singleton.get_dictionary()
        assert "zero" not in corpus_dict
        assert len(corpus_dict) == 5

    def test_get_dictionary_len(self):
        corpus_dict = self.corpus_singleton.get_dictionary()
        assert len(corpus_dict) == 5

    def test_get_tokens_in_document_max(self):
        ngram = self.corpus_singleton.vectorizer.transform([self.search])
        nr_tokens = self.corpus_singleton.get_tokens_in_document(ngram, 0)
        assert nr_tokens <= ngram.sum()

    def test_get_tokens_in_document_min(self):
        ngram = self.corpus_singleton.vectorizer.transform([self.search])
        nr_tokens = self.corpus_singleton.get_tokens_in_document(ngram, 0)
        assert nr_tokens >= 0

    def test_get_best_match_sort_desc(self):
        result = self.corpus_multiple.get_matching_documents(self.search)
        assert result[0]['score'] >= result[1]['score']

    def test_get_best_match_no_match(self):
        result = self.corpus_multiple.get_matching_documents("invalid")
        assert len(result) == 0

    def test_get_best_match_full_score(self):
        result = self.corpus_multiple.get_matching_documents(self.content)
        assert result[0]['score'] == len(self.content.split())

    def test_get_best_match_nr_search_tokens_is_max(self):
        """test that the maximum score is no higher than the number of words in the search string"""
        result = self.corpus_multiple.get_matching_documents(self.search)
        assert result[0]['score'] <= len(self.search.split())

    def test_apply_floor_zero(self):

        input_csr = csr_matrix(np.array([0, -1, 1]))
        expected_csr = csr_matrix(np.array([0, 0, 1])).toarray()
        result_csr = Corpus.apply_floor_zero(input_csr)
        assert str(result_csr) == str(expected_csr)