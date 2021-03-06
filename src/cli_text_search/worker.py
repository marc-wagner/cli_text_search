import json
import os
import sys

import flask
from flask import Flask, request
from flasgger import Swagger

from distributed_corpus import DistributedCorpus

app = Flask(__name__)
swagger = Swagger(app)
#app.debug = True

initialized = False
corpus = None
worker_id = -1


@app.route('/init', methods=['POST'])
def init():
    """
    parameters:
      - name: filenames
        type: string
        required: true
    responses:
      200:
        description: the worker_id and the number of indexed documents
        examples:
          data: {'worker_id': 0, "indexed_documents": 1000}
    """
    global initialized
    global worker_id
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        data = json.loads(request.data)
        print(f"worker id: {worker_id} of type {type(worker_id)}")
        print(f"vs post data worker id: {data['worker_id']} of type {type(data['worker_id'])}")
        assert data["worker_id"] == int(worker_id)
        if not initialized:
            args = request.args
            global corpus
            corpus = DistributedCorpus(data['file_paths'], "filename")
            initialized = True
            worker_id = data["worker_id"]
        return json.dumps({'worker_id': worker_id, "indexed_documents": corpus.nr_documents_loaded})

    else:
        return 'Content-Type not supported!'


@app.route('/search', methods=['GET'])
def search():
    """
    The function takes a query and returns a list of matching documents
    :params q: search string
    :params max_results: maximum number of matching documents to return
    :return: A JSON object containing the matching documents.
    """
    args = request.args
    if initialized:
        if "max_results" in args:
            result = json.dumps(corpus.get_matching_documents(args["q"], args["max_results"]))
        else:
            result = json.dumps(corpus.get_matching_documents(args["q"]))
        return result
    else:
        return flask.Response("worker has not been initialized. send POST to /init first.", status=500)


if __name__ == '__main__':
    worker_id = sys.argv[1]
    port = os.environ.get(f"WORKER_PORT_{str(worker_id)}")
    app.run(port=port)
