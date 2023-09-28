import argparse
import sys
from typing import Optional


def run_console(dir_path: Optional[str] = None, verbose: bool = False) -> None:
    """
    :param dir_path: directory to search for garbage;
    :param verbose: if True, then searcher will display found junk in real mode.
    """

    from console import Menu

    menu = Menu(verbose)
    menu.run(dir_path)


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
    parser.add_argument("--verbose", "-v", action="store_true", default=False, help="Searcher will display found junk "
                                                                                    "in real mode")
    parsed_args = parser.parse_args(sys.argv[1:])
    if parsed_args.gui:
        run_gui()
    else:
        run_console(parsed_args.dir, parsed_args.verbose)
