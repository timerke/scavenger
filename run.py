import argparse
import sys
from searcher import Searcher


def main(dir_path: str) -> None:
    """
    :param dir_path: directory to search for garbage.
    """

    searcher = Searcher()
    searcher.search_junk(dir_path)
    searcher.print_junk()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script for searching junk files and directories")
    parser.add_argument("--dir", type=str, default=None, help="Directory to search for garbage")
    parsed_args = parser.parse_args(sys.argv[1:])
    main(parsed_args.dir)
