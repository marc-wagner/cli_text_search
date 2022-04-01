"""
unit tests for Corpus class
"""
import numpy as np

from cli_text_search.corpus import Corpus


def test_get_document_term_matrix():
    assert False


def test_get_dictionary():
    assert False


def test_get_tokens_in_document():
    assert False


def test_get_best_match():
    assert False


def test_apply_floor_zero():

    input_array = np.ndarray(shape=(1, 3),
                             buffer=np.array([0, -1, 1]),
                             dtype=int)

    expected_array = np.ndarray(shape=(1, 3),
                                buffer=np.array([0, 0, 1]),
                                dtype=int)

    result_array = Corpus.apply_floor_zero(input_array)

    assert result_array == expected_array
