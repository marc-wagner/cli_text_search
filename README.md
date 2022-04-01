# cli_text_search

### search for words in a collection of text documents using command line

this program is a bare-bones text search engine for text files. <br/> 
pass a directory to search as argument  <br/>
then type search sentences in interactive command line prompt to view most relevant documents

## Use

> from within a terminal

```
python ./src/cli_text_search/main.py [document_directory]

search > type sentence
 
or type 'quit' to exit
```

## Document Search Score

Score is calculated on the occurrence of search words<br/>
irrelevant of their frequency of occurrence<br/>
1-letter words are ignored<br/>
the order of the words is ignored<br/>  
this deviates from the industry-standard DF-ITF scoring

## Data structure

the common dictionary across all documents is the bottleneck in terms of memory usage.<br>    
SciKit Learn's compact sparse rows matrix is used as the primary data structure
to build a dictionary of all words within each document.<br/>

This reflects the shape of the data: long rows with number of words = O(2) number of documents
The data structure is efficient in-memory because it only saves non-zero elements as int.<br/> 

If the number of documents and words exceeds the memory capacity, a distributed version
of the dictionary could be implemented using the feature_extraction.text.HashingVectorizer
but that would introduce a risk of collision (false positives). cf<br/>

https://scikit-learn.org/stable/auto_examples/applications/plot_out_of_core_classification.html#sphx-glr-auto-examples-applications-plot-out-of-core-classification-py

## Note

This project has been set up using PyScaffold 4.2.1. <br/>
For details and usage information on PyScaffold see https://pyscaffold.org/.