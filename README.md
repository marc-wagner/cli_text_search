# cli_text_search

### search for words in a collection of text documents using command line

this program is a bare-bones text search engine for text files. <br/> 
pass a directory as argument  <br/>
then type search sentences in interactive command line prompt to view most relevant documents

## Use

> from within a terminal

```
python ./src/cli_text_search/main.py [document_directory]

search > type sentence
 
or type 'quit' to exit
```

## Search Score

The score is calculated on the occurrence of search words<br/>
irrelevant of their frequency of occurrence<br/>
1-letter words are ignored<br/>
the order of the words is ignored<br/>  
this deviates from the industry-standard DF-ITF scoring

###Example:

given a document with content:
```
"one two three three four five" 
  
```
if you search for
```
two times three is six 
```
the score will be 40 % (2 / 5) , as there are 2 overlaps ('two','three') and 5 words in the search string  

## Data structure

the common dictionary across all documents is the bottleneck in terms of memory usage.<br>    
SciKit Learn's compact sparse rows matrix is used as the primary data structure
to efficiently store the occurrence of each word within each document.<br/>
```
<class 'scipy.sparse._csr.csr_matrix'>
```

This reflects the shape of the data: long rows with number of words = O(2) number of documents
The data structure is efficient in-memory because it only saves non-zero elements as int.<br/> 

```
shape: (13, 14902)

Data view: 
  (0, 9381)	    82
  (0, 9602)	    3
  (0, 14765)	35
  (0, 1286)	    421
  :	            :
  (12, 1304)	1
  (12, 5271)	1
  (12, 10439)	1
  (12, 13531)	1
```

The requirement is to load the documents in memory.

If the number of documents and words exceeds the memory capacity, a distributed version
of the dictionary could be implemented using the feature_extraction.text.HashingVectorizer
that would introduce a mild risk of collision (false positives). cf<br/>

https://scikit-learn.org/stable/auto_examples/applications/plot_out_of_core_classification.html#sphx-glr-auto-examples-applications-plot-out-of-core-classification-py

## Note

This project has been set up using PyScaffold 4.2.1. <br/>
For details and usage information on PyScaffold see https://pyscaffold.org/.