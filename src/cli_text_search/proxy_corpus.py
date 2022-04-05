import asyncio
import json
import logging
import os

import pandas as pd
import numpy as np
import requests

from corpus import Corpus


# async def create_proxy_corpus(input, input_type="filename"):
#     corpus = ProxyCorpus(input, input_type)
#     await corpus._init()
#     return corpus


class ProxyCorpus(Corpus):
    """Proxy for remote Corpus.
    uses HTTP requests to initialize workers and to run search on workers
    Note: workers must have access to shared document filepath

    Methods:
        __init__(self, input, input_type="content")
        get_document_term_matrix(self)
        get_tokens_in_document(self, search_ngram, document_index)
        get_matching_documents(self, search_term)
    """

    nr_workers = 1

    @classmethod
    async def create(cls, file_paths, input_type):
        self = ProxyCorpus(file_paths, input_type)
        await self.prepare(file_paths, input_type)
        return self

    def __init__(self, input, input_type="filename"):
        """
        split documents into chunks and initialize workers that manage each chunk
        workers are initialized via HTTP GET request and return the number of documents that they manage

        :param input: list of document filenames
        :returns: corpus object
        """
        # TODO increment this asynchronously
        self.nr_documents_loaded = 0  #initialize dictionary
        if input_type != "filename":
            raise SyntaxError("input_type for ProxyCorpus should be 'filename'")
        self.documents = input  # required to extract row labels from sparse matrix
        logging.debug(f"started initializing {self.nr_workers} workers")

    async def prepare(self, file_paths, input_type):
        """
        The function takes a list of file paths, splits it into chunks, and
        then assigns each chunk to a worker. The function then waits for all workers to finish their work and returns the
        corpus

        :param file_paths: The list of files to be processed
        """
        chunk_size = int(round(len(file_paths) / self.nr_workers, 0))
        msgs = await asyncio.gather(*(self.init_remote_corpus(input=file_paths[i * chunk_size: (i+1) * chunk_size:],
                                                              input_type=input_type,
                                                              worker=i) for i in range(self.nr_workers)))
        logging.info("\n".join(msgs))

    async def init_remote_corpus(self, input, input_type, worker):
        """
        It takes a list of file paths and sends them to a remote worker

        :param input: a list of file paths to be processed by the worker
        :param input_type: the type of input data. It can be "file" or "dir"
        :param worker: the worker id
        :return: The result of the remote call to init_remote_corpus
        """
        logging.debug(f"worker: {worker}")
        if len(input) == 0:
            raise RuntimeError("input data is an empty list")
        route = '/init'
        headers = {'Content-type': 'application/json'}
        url = os.environ.get(f"WORKER_HOST_{worker}") + ":" + os.environ.get(f"WORKER_PORT_{worker}") + route
        body = json.dumps({"worker_id": worker, "file_paths": input})
        logging.debug(f"sending http POST request to worker {worker} at {url}")
        res = requests.post(url, body, headers=headers)
        res.raise_for_status()
        logging.debug(f"received http response from {url} with status code {res.status_code}")
        return res.json()['result']

    def get_document_term_matrix(self):
        """view matrix that matches hash_buckets to documents
        row headers = documents
        column headers = hash buckets
        data = occurrences of hashed term in 'document'

        returns: pandas.dataFrame
        """
        # TODO implement this
        return pd.DataFrame(data=np.zeros((1,1)))

    def get_dictionary(self):
        """does not exist for proxy corpus
        rType:
        """
        raise AttributeError(f"cannot implement parent function {type(super)}:get_dictionary() in {type(self)}")

    async def get_matching_documents(self, search_term):
        logging.debug(f"searching for '{search_term}' in :{len(self.documents)} documents")
        score = []
        route = '/search'
        params = {'q': search_term}
        for worker in range(0, self.nr_workers):
            url = os.environ.get(f"WORKER_HOST_{worker}") + ":" + os.environ.get(f"WORKER_PORT_{worker}") + route
            logging.debug(f"sending http POST request to worker {worker} at {url}")
            res = requests.get(url, params)
            res.raise_for_status()
            logging.debug(f"received http response from {url} with status code {res.status_code}")
            score.append(res.json())
        logging.debug(f"returning {len(score)} matches")
        return score
