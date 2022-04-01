import os
import pytest
from cli_text_search import corpus
from cli_text_search import main

content = "one one one two three four five"
multi_content = ["one one one two three four five", "one two three four"]
search = "four five six"
corpus_singleton = corpus.Corpus([content])
corpus_multiple = corpus.Corpus(multi_content)

def test_collect_file_paths_no_binary(tmp_path):
    """
    test a binary file is skipped during collection
    """
    # TODO find a more robust way to detect binary files
    os.chdir(tmp_path)
    f = open('binary_file', 'w+b')
    byte_arr = [120, 3, 255, 0, 100]
    binary_format = bytearray(byte_arr)
    f.write(binary_format)
    f.close()
    result = main.collect_file_paths(tmp_path)
    assert len(result) == 0


def test_collect_file_paths_subdirectory(tmp_path):
    """
    test a text file in a subdirectory is read during collection
    """
    os.chdir(tmp_path)
    os.mkdir("subdirectory")
    f = open('subdirectory/text_file', 'w')
    content = "plain text"
    f.write(content)
    f.close()
    result = main.collect_file_paths(tmp_path)
    assert result.pop()[-23:] == "/subdirectory/text_file"


def test_search_score():
    result = main.search(search, corpus_multiple)
    expected ="""one one one two three four five : 67.0% 
one two three four : 33.0% 
"""
    assert result == expected


def test_search_tokens():
    result = main.search(search, corpus_singleton)
    percentage = result[-7:-3]
    nr_overlaps = 2 # overlap between 'search' and 'content' = ('four', 'five')
    assert percentage == str(round(100.0 * nr_overlaps / len(search.split()),0))


def test_invoke_prompt_no_text():
    directory = "invalid"
    with pytest.raises(Exception):
        main.invoke_prompt(directory)


def test_invoke_prompt_quit():
    # TODO add fixture for import toolkit above
    assert False


def test_main_no_path():
    """
    raise error if no path is provided
    """
    argv = []
    with pytest.raises(Exception):
        main.main(argv)


