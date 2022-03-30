"""
This is a skeleton file that can serve as a starting point for a Python
console script. To run this script uncomment the following lines in the
``[options.entry_points]`` section in ``setup.cfg``::

    console_scripts =
         fibonacci = cli_text_search.skeleton:run

Then run ``pip install .`` (or ``pip install -e .`` for editable mode)
which will install the command ``fibonacci`` inside your current environment.

Besides console scripts, the header (i.e. until ``_logger``...) of this file can
also be used as template for Python modules.

Note:
    This skeleton file can be safely removed if not needed!

References:
    - https://setuptools.pypa.io/en/latest/userguide/entry_point.html
    - https://pip.pypa.io/en/stable/reference/pip_install
"""

import logging
import sys

from prompt_toolkit import PromptSession

_logger = logging.getLogger(__name__)
logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
logging.basicConfig(level="DEBUG",
                    stream=sys.stdout,
                    format=logformat,
                    datefmt="%Y-%m-%d %H:%M:%S")

# ---- Python API ----


# ---- CLI ----
def invoke_prompt(folder_path):
    # TODO: user folder_path
    print(f"input path: {folder_path}")
    s = PromptSession(message='search> ')
    while True:
        answer = s.prompt()
        # TODO: insert your implementation here


def main(argv):
    f = argv[1] if len(argv) > 1 else None
    if f:
        invoke_prompt(f)
    else:
        raise Exception('Missing parameter: folder_path')


if __name__ == '__main__':
    main(sys.argv)
