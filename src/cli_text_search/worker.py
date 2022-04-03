import json
from flask import Flask, request

from src.cli_text_search.distributed_corpus import DistributedCorpus

app = Flask(__name__)

initiated = False
corpus = None

@app.route('/init', methods=['POST'])
def init():
    global initiated
    if not initiated:
        args = request.args
        global corpus
        corpus = DistributedCorpus(data,"filename")
        initiated = True
    return json.dumps({'result': f"worker is indexing {corpus.nr_documents_loaded}"})


@app.route('/search', methods=['GET'])
def search():
    args = request.args
    return json.dumps(corpus.get_matching_documents(search_term, max_len_result))


app.run()
