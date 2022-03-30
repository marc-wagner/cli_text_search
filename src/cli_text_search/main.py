import logging
import sys

from prompt_toolkit import PromptSession

logger = logging.getLogger(__name__)
logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
logging.basicConfig(level="DEBUG",
                    stream=sys.stdout,
                    format=logformat,
                    datefmt="%Y-%m-%d %H:%M:%S")

# ---- Python API ----


# ---- CLI ----
def invoke_prompt(folder_path):
    # TODO: user folder_path
    logger.info(f"input path: {folder_path}")

    # TO DO handle cases with multiple subdirectories

    # TO DO generate metadata for each file

    s = PromptSession(message='search> ')
    while True:
        logger.info(f"starting interactive user prompt")
        answer = s.prompt()
        # TODO: insert your implementation here


def main(argv):
    f = argv[1] if len(argv) > 1 else None
    if f:
        invoke_prompt(f)
    else:
        raise Exception('Missing parameter: folder_path')


if __name__ == '__main__':
    main(sys.argv)
