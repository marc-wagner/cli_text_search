import asyncio
import logging
import os
import sys
import http
from prompt_toolkit import PromptSession

from cli_text_search.corpus import Corpus
from cli_text_search.proxy_corpus import ProxyCorpus

logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
logging.basicConfig(level="INFO",
                    stream=sys.stdout,
                    format=logformat,
                    datefmt="%Y-%m-%d %H:%M:%S")
http.client.HTTPConnection.debuglevel = 0


max_results = 10  # max number of results returned


# ---- Python API ----
def collect_file_paths(directory):
    """
    Given a directory, return a list of all the files in that directory and its subdirectories

    :param directory: the directory that holds the text files to be used in the corpus
    :return: A list of file paths
    """
    text_file_paths = []
    for dirpath, dirnames, files in os.walk(directory):
        for name in files:
            file_path = os.path.join(dirpath, name)
            try:
                text_file = open(file_path, "r")
                logging.debug(f"found file {file_path}")
            except UnicodeEncodeError:
                logging.warning(f"could not open file {file_path}")
            except OSError:
                logging.warning(f"could not open file {file_path}")
            finally:
                text_file.close()
                text_file_paths.append(file_path)
    logging.info(f"found {len(text_file_paths)} files in directory {directory}")
    return text_file_paths


async def search(answer, corpus):
    """search for string in all documents in corpus.
    tokenize search term and score documents based on presence of each search word

    :param answer: search string to be found
    :param corpus: collection of documents to search in
    :returns: formatted text of documents and their score
    :rType: String
    """
    search_tokens = Corpus([answer], input_type="content")
    nr_tokens = len(search_tokens.get_dictionary())
    logging.debug(f"number of (unique) tokens in search: {nr_tokens}")
    tokens_as_string = ' '.join(search_tokens.get_dictionary().flatten())
    if type(corpus) == ProxyCorpus:
        document_score = await corpus.get_matching_documents(search_term=tokens_as_string)
    else:
        document_score = corpus.get_matching_documents(search_term=tokens_as_string)
    output = ''
    if len(document_score) == 0:
        return "no matches found"
    for result in document_score[0: max_results]:
        output += f"{result['document']} : {round(100.0 * result['score']/nr_tokens,0)}% \n"
    return output


async def build_corpus(folder_path, big):
    logging.debug(f"input path: {folder_path}")
    file_paths = collect_file_paths(folder_path)
    logging.debug(f"len filepaths: {len(file_paths)}")
    if len(file_paths) == 0:
        raise FileNotFoundError(f"no text files found in directory {folder_path}")
    if big:
        corpus = await ProxyCorpus.create(file_paths, input_type="filename")
    else:
        corpus = Corpus(file_paths, input_type="filename")
    return corpus


async def invoke_prompt(folder_path, big=False):
    """manage program workflow and prompt:
        first load corpus of documents,
        then loop: prompt for search term, show matching documents
        until the user types 'quit'

        :param folder_path: directory that contains documents to search in
        :param big: launch search on a distributed system
        :returns: None
    """
    corpus = await build_corpus(folder_path, big)

    loop = True
    logging.debug(f"starting interactive user prompt")
    s = PromptSession(message="'search (type 'quit' to exit) > ")
    while loop:
        answer = await s.prompt_async()
        try:
            if answer == "quit":
                logging.info(f"user requested to quit program execution")
                loop = False
            else:
                print(await search(answer, corpus))
        except LookupError:
            logging.error(f"lookup error for search term '{answer}'")


# ---- CLI ----
async def main(argv):
    f = argv[len(argv)-1] if len(argv) > 1 else None
    if f:
        big = (argv[1] == '--big')
        await invoke_prompt(f, big)
    else:
        raise Exception('Missing parameter: folder_path')


if __name__ == '__main__':
    asyncio.run(main(sys.argv))
