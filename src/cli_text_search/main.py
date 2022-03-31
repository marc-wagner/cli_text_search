import logging
import os
import sys
from prompt_toolkit import PromptSession

from cli_text_search.corpus import Corpus

logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
logging.basicConfig(level="DEBUG",
                    stream=sys.stdout,
                    format=logformat,
                    datefmt="%Y-%m-%d %H:%M:%S")

max_results = 10  # max number of results returned

# ---- Python API ----
def collect_file_paths(directory):
    text_file_paths = []
    for dirpath, dirnames, files in os.walk(directory):
        for name in files:
            file_path = os.path.join(dirpath, name)
            logging.debug(f"found file {file_path}")
            text_file_paths.append(file_path)

    return text_file_paths


def invoke_prompt(folder_path):
    """
    manage program workflow:
        first load corpus for search
        then loop: prompt for search term, show matching documents
        until the user types 'quit'
    """
    logging.info(f"input path: {folder_path}")

    file_paths = collect_file_paths(folder_path)

    # TODO make this asynch
    corpus = Corpus(file_paths, input_type="filepath")

    loop = True
    logging.info(f"starting interactive user prompt")
    s = PromptSession(message='search> ')
    while loop:
        try:
            #answer = "have you seen my dogs dogs dogs?"
            answer = s.prompt()

            if answer == "quit":
                logging.info(f"user requested to quit program execution")
                loop = False
            else:
                search(answer, corpus)
        except LookupError:
            logging.error(f"lookup error for search term '{answer}'")


def search(answer, corpus):
    """

    """
    search_tokens = Corpus([answer], input_type="string")
    nr_tokens = len(search_tokens.get_dictionary())
    logging.debug(f"number of (unique) tokens in search: {nr_tokens}")
    tokens_as_string = ' '.join(search_tokens.get_dictionary().flatten())
    document_score = corpus.get_best_match(search_term=tokens_as_string, max_rank=max_results)
    for result in document_score:
        print(f"{100.0 * result[0]/nr_tokens}% : {result[1]}")


# ---- CLI ----
def main(argv):
    # assuming only 1 path is provided
    # TODO validate 1 path assumption
    f = argv[1] if len(argv) > 1 else None
    if f:
        invoke_prompt(f)
    else:
        raise Exception('Missing parameter: folder_path')


if __name__ == '__main__':
    main(sys.argv)
