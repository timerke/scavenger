import argparse
import sys
from typing import Optional
from searcher import Searcher


def run_console(dir_path: Optional[str] = None) -> None:
    """
    :param dir_path: directory to search for garbage.
    """

    searcher = Searcher()
    searcher.search_junk(dir_path)
    searcher.print_junk()


def run_gui() -> None:
    from PyQt5.QtWidgets import QApplication
    from gui import MainWindow

    app = QApplication(sys.argv[1:])
    window = MainWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script for searching junk files and directories")
    parser.add_argument("--dir", type=str, default=None, help="Directory to search for garbage")
    parser.add_argument("--gui", action="store_true", default=False, help="Run script from GUI")
    parsed_args = parser.parse_args(sys.argv[1:])
    if parsed_args.gui:
        run_gui()
    else:
        run_console(parsed_args.dir)
