import logging
import os
import sys

from prompt_toolkit import PromptSession

logger = logging.getLogger(__name__)
logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
logging.basicConfig(level="DEBUG",
                    stream=sys.stdout,
                    format=logformat,
                    datefmt="%Y-%m-%d %H:%M:%S")


# ---- Python API ----
def collect_files(directory):
    text_files = []
    for dirpath, dirnames, files in os.walk(directory):
        for name in files:
            file_path = os.path.join(dirpath, name)
            logger.debug(f"found file {file_path}")
            text_files.append((name, file_path))

    return text_files


def invoke_prompt(folder_path):
    """
    load corpus for search
    and prompt for search term
    """
    # TODO: user folder_path
    logger.info(f"input path: {folder_path}")

    documents = collect_files(folder_path)
    # TODO generate metadata for each file
    # TODO asynch for metadata


    s = PromptSession(message='search> ')
    while True:
        try:
            logger.info(f"starting interactive user prompt")
            answer = s.prompt()

            # TODO: insert your implementation here
            logger.info(f"searching best match for {answer} in {len(documents)} documents")
            ranked_documents = ranked_search(answer, documents)
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
