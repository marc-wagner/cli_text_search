"""
unit tests for Corpus class
"""
import pytest

from src.cli_text_search.distributed_corpus import DistributedCorpus


class TestDistributedCorpus:

    content = "one one one two three four five"
    multi_content = ["one one one two three four five", "one two three four"]
    search = "four five six"
    corpus_singleton = DistributedCorpus([content])
    corpus_multiple = DistributedCorpus(multi_content)

    def test_get_dictionary_error(self):
        with pytest.raises(Exception):
            self.corpus_singleton.get_dictionary()

    def test_get_best_match_sort_desc(self):
        result = self.corpus_multiple.get_matching_documents(self.search)
        assert result[0]['score'] >= result[1]['score']

    def test_get_best_match_no_match(self):
        result = self.corpus_multiple.get_matching_documents("invalid")
        assert len(result) == 0

    def test_get_best_match_nr_search_tokens_is_max(self):
        """test that the maximum score is no higher than the number of words in the search string"""
        result = self.corpus_multiple.get_matching_documents(self.search)
        assert result[0]['score'] <= len(self.search.split())
