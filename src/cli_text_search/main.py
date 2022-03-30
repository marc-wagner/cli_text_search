import logging
import os
import sys
from IPython.display import display
from prompt_toolkit import PromptSession

from src.cli_text_search.corpus import Corpus

logger = logging.getLogger(__name__)
logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
logging.basicConfig(level="DEBUG",
                    stream=sys.stdout,
                    format=logformat,
                    datefmt="%Y-%m-%d %H:%M:%S")




def tokenize(sentence):
    sentence.lower()
    return


# ---- Python API ----
def collect_file_paths(directory):
    text_file_paths = []
    for dirpath, dirnames, files in os.walk(directory):
        for name in files:
            file_path = os.path.join(dirpath, name)
            logger.debug(f"found file {file_path}")
            # TODO discard binary files, read all other
            text_file_paths.append(file_path)

    return text_file_paths


def invoke_prompt(folder_path):
    """
    load corpus for search
    and prompt for search term
    """
    logger.info(f"input path: {folder_path}")

    file_paths = collect_file_paths(folder_path)
    # TODO generate metadata for each file
    corpus = Corpus(file_paths)
    # TODO asynch for metadata
    display(corpus.df_dtm)

    s = PromptSession(message='search> ')
    while True:
        try:
            logger.info(f"starting interactive user prompt")
            answer = "purpose"  # s.prompt()

            logger.info(f"searching best match for {answer} in {len(corpus.documents)} documents")
            ranked_documents = corpus.get_best_match(search_term=answer, max_rank=10)
        except LookupError:
            logger.error(f"lookup error for search term {answer}")


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
