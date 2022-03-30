import pytest

from cli_text_search.skeleton import main

__author__ = "marc"
__copyright__ = "marc"
__license__ = "MIT"


def test_fib():
    """API Tests"""
    assert fib(1) == 1
    assert fib(2) == 1
    assert fib(7) == 13
    with pytest.raises(AssertionError):
        fib(-10)


def test_main(capsys):
    """CLI Tests"""
    # capsys is a pytest fixture that allows asserts agains stdout/stderr
    # https://docs.pytest.org/en/stable/capture.html
    main(["./"])
    captured = capsys.readouterr()
    assert "skeleton.py" in captured.out


def test_invoke_prompt():
    assert False


def test_main():
    assert False
