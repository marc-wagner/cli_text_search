.. These are examples of badges you might want to add to your README:
   please update the URLs accordingly

.. image:: https://img.shields.io/badge/-PyScaffold-005CA0?logo=pyscaffold
    :alt: Project generated with PyScaffold
    :target: https://pyscaffold.org/

## cli_text_search

    search for words in a collection of text documents using command line


this program is a bare-bones text search engine for text files. It uses

## Use

```bash
python ./src/cli_text_search/main.py [document_directory]
search > type sentence 
or type 'quit' to exit
```

## Relevance Scoring

Score is calculated on the occurrence of search words
irrelevant of their frequency of occurrence
1-letter words are ignored
the order of the words is ignored
this deviates from the industry-standard DF-ITF scoring

## Data structure

SciKit Learn's compact sparse rows matrix is used as the primary data structure
to build a dictionary of all words within each document.
This reflects the shape of the data: number of words = O(2) number of documents
The data structure is efficient in-memory because it only saves non-zero elements as int 

the common dictionary across all documents is the bottleneck in terms of memory usage.
It uses a sparse representation of a single datatype, in this case int.

https://scikit-learn.org/stable/auto_examples/applications/
plot_out_of_core_classification.html#sphx-glr-auto-examples-
applications-plot-out-of-core-classification-py

## Note

This project has been set up using PyScaffold 4.2.1. For details and usage
information on PyScaffold see https://pyscaffold.org/.