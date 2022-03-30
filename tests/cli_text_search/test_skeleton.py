import pytest
import importlib
import sys

from cli_text_search import skeleton

__author__ = "marc"
__copyright__ = "marc"
__license__ = "MIT"


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
