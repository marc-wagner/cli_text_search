.. These are examples of badges you might want to add to your README:
   please update the URLs accordingly

    .. image:: https://api.cirrus-ci.com/github/marc-wagner/cli_text_search.svg?branch=main
        :alt: Built Status
        :target: https://cirrus-ci.com/github/marc-wagner/cli_text_search
    .. image:: https://readthedocs.org/projects/cli_text_search/badge/?version=latest
        :alt: ReadTheDocs
        :target: https://cli_text_search.readthedocs.io/en/stable/
    .. image:: https://img.shields.io/coveralls/github/<USER>/cli_text_search/main.svg
        :alt: Coveralls
        :target: https://coveralls.io/r/<USER>/cli_text_search
    .. image:: https://img.shields.io/pypi/v/cli_text_search.svg
        :alt: PyPI-Server
        :target: https://pypi.org/project/cli_text_search/
    .. image:: https://img.shields.io/conda/vn/conda-forge/cli_text_search.svg
        :alt: Conda-Forge
        :target: https://anaconda.org/conda-forge/cli_text_search
    .. image:: https://pepy.tech/badge/cli_text_search/month
        :alt: Monthly Downloads
        :target: https://pepy.tech/project/cli_text_search
    .. image:: https://img.shields.io/twitter/url/http/shields.io.svg?style=social&label=Twitter
        :alt: Twitter
        :target: https://twitter.com/cli_text_search

.. image:: https://img.shields.io/badge/-PyScaffold-005CA0?logo=pyscaffold
    :alt: Project generated with PyScaffold
    :target: https://pyscaffold.org/

===============
cli_text_search
===============


    search for words in a collection of text documents using command line


this program is a bare-bones text search engine for text files.

===
Use
===

.. code:: bash
   > python main.py <document_directory>

   > [CTRL+C] to exit

Relevance Scoring
-----------------

Score is calculated on the occurrence of search words, irrelevant of their frequency of occurrence
1-letter words are ignored


.. _pyscaffold-notes:

Data structure
--------------
SciKit Learn's compact sparse rows matrix is used as the primary data structure
to build a dictionary of all words within each document.
this dictionary is the bottleneck in terms of memory usage.
It uses a sparse representation of a single datatype, in this case int.

https://scikit-learn.org/stable/auto_examples/applications/
plot_out_of_core_classification.html#sphx-glr-auto-examples-
applications-plot-out-of-core-classification-py


Note
====



This project has been set up using PyScaffold 4.2.1. For details and usage
information on PyScaffold see https://pyscaffold.org/.