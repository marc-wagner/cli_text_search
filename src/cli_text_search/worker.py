import json
import os

from flask import Flask, request

from distributed_corpus import DistributedCorpus

app = Flask(__name__)
app.debug = True

initiated = False
corpus = None
worker_id = -1


@app.route('/init', methods=['POST'])
def init():
    global initiated
    global worker_id
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        data = json.loads(request.data)
        if not initiated:
            args = request.args
            global corpus
            corpus = DistributedCorpus(data['file_paths'], "filename")
            initiated = True
            worker_id = data["worker_id"]
        return json.dumps({'result': f"worker {worker_id} is indexing {corpus.nr_documents_loaded} documents"})

    else:
        return 'Content-Type not supported!'


@app.route('/search', methods=['GET'])
def search():
    args = request.args
    if "max_results" in args:
        result = json.dumps(corpus.get_matching_documents(args["q"], args["max_results"]))
    else:
        result = json.dumps(corpus.get_matching_documents(args["q"]))
    return result


app.run(port=os.environ.get('PORT'))
