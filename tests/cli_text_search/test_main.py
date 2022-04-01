import os
import pytest

from cli_text_search import main

def test_collect_file_paths_no_binary(tmp_path):
    """
    test a binary file is skipped during collection
    """
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
    assert False


def test_search_tokens():
    assert False


def test_invoke_prompt_no_text():
    assert False


def test_invoke_prompt_quit():
    assert False


def test_main_no_path():
    """
    raise error if no path is provided
    """
    argv = []
    with pytest.raises(Exception):
        main.main(argv)


