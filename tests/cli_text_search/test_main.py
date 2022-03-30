import pytest

from cli_text_search import main


def test_invoke_prompt():
    assert False


def test_main_no_path():
    """
    raise error if no path is provided
    """
    argv = []
    with pytest.raises(Exception):
        main.main(argv)


def test_collect_files():
    """
    test recursion works completely
    """
    assert False
