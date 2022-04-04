import json
from flask import Flask, request

from src.cli_text_search.distributed_corpus import DistributedCorpus

app = Flask(__name__)
app.debug = True

initiated = False
corpus = None


@app.route('/init', methods=['POST'])
def init():
    global initiated
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        data = json.loads(request.data)
        if not initiated:
            args = request.args
            global corpus
            corpus = DistributedCorpus(data['file_paths'], "filename")
            initiated = True
        return json.dumps({'result': f"worker is indexing {corpus.nr_documents_loaded} documents"})

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


app.run()
