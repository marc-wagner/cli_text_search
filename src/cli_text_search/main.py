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
    """
    build a list of valid text files to be used in corpus
    """
    text_file_paths = []
    for dirpath, dirnames, files in os.walk(directory):
        for name in files:
            try:
                file_path = os.path.join(dirpath, name)
                text_file = open(file_path, "r")
                logging.debug(f"found file {file_path}")
            except UnicodeEncodeError:
                logging.warning(f"could not open file {file_path}")
            except OSError:
                logging.warning(f"could not open file {file_path}")
            finally:
                text_file.close()
                text_file_paths.append(file_path)
    logging.info(f"found {len(text_file_paths)} files in directory")
    return text_file_paths


def search(answer, corpus):
    """
    search for string in all documents in corpus.
    tokenize search term and score documents based on presence of each search word
    return formatted text of documents and their score
    """
    search_tokens = Corpus([answer], input_type="string")
    nr_tokens = len(search_tokens.get_dictionary())
    logging.debug(f"number of (unique) tokens in search: {nr_tokens}")
    tokens_as_string = ' '.join(search_tokens.get_dictionary().flatten())
    document_score = corpus.get_best_match(search_term=tokens_as_string, max_rank=max_results)
    output = ''
    if len(document_score) == 0:
        return "no matches found"
    for result in document_score:
        output += f"{result[1]} : {round(100.0 * result[0]/nr_tokens,0)}% \n"
    return output


def invoke_prompt(folder_path):
    """
    manage program workflow and prompt:
        first load corpus of documents,
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
            #answer = "have you seen my dogs dogs and cats?"
            answer = s.prompt()

            if answer == "quit":
                logging.info(f"user requested to quit program execution")
                loop = False
            else:
                print(search(answer, corpus))
        except LookupError:
            logging.error(f"lookup error for search term '{answer}'")


# ---- CLI ----
def main(argv):
    f = argv[1] if len(argv) > 1 else None
    if f:
        invoke_prompt(f)
    else:
        raise Exception('Missing parameter: folder_path')


if __name__ == '__main__':
    main(sys.argv)
