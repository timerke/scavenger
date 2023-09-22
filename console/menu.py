from typing import Any, List, Optional
from searcher import Searcher, utils as ut


class Menu:
    """
    Class with menu for working in terminal.
    """

    def __init__(self, verbose_mode: bool = False) -> None:
        """
        :param verbose_mode: if True, then searcher will display found junk in real mode.
        """

        self._junk: List[str] = []
        self._searcher: Searcher = Searcher(verbose_mode)

    @staticmethod
    def _exit() -> int:
        ut.print_("Exit")
        return 1

    @staticmethod
    def _get_answer_to_remove() -> bool:
        while True:
            ut.print_("Your choice: ", end="")
            user_answer = input().lower()
            if user_answer in ("y", "n"):
                return user_answer == "y"
            ut.print_("Unknown choice. Try again")

    @staticmethod
    def _get_directory_to_search() -> str:
        """
        :return: directory in which to search for junk.
        """

        ut.print_("In which directory to search junk (by default in current directory)?")
        dir_path = input()
        if not dir_path:
            dir_path = "."
        return dir_path

    def _get_task(self) -> Any:
        """
        :return: result of command that user selected.
        """

        tasks = {"s": self._search_junk,
                 "a": self._remove_all,
                 "o": self._remove_one_by_one,
                 "q": self._exit}
        while True:
            ut.print_("Your choice: ", end="")
            user_answer = input().lower()
            task = tasks.get(user_answer, None)
            if task is not None:
                return task()
            ut.print_("Unknown choice. Try again")

    def _remove_all(self) -> None:
        ut.print_("Removing all found junk files and directories...")
        if self._junk:
            for file_or_dir in self._junk:
                try:
                    self._searcher.remove(file_or_dir)
                except Exception:
                    ut.print_(f"Error: failed to remove '{file_or_dir}'")
            self._junk.clear()
        else:
            ut.print_("No junk to remove")

    def _remove_one_by_one(self) -> None:
        ut.print_("Removing found junk files and directories one by one...")
        if self._junk:
            for file_or_dir in self._junk:
                ut.print_(f"Remove '{file_or_dir}' (y/n)?")
                if self._get_answer_to_remove():
                    try:
                        self._searcher.remove(file_or_dir)
                    except Exception:
                        ut.print_(f"Error: failed to remove '{file_or_dir}'")
            self._junk.clear()
        else:
            ut.print_("No junk to remove")

    def _search_junk(self, dir_path: Optional[str] = None) -> None:
        """
        :param dir_path: directory in which to search for junk.
        """

        if dir_path is None:
            dir_path = self._get_directory_to_search()
        ut.print_(f"Searching for junk in directory '{dir_path}'...")
        self._junk = self._searcher.search_junk(dir_path)
        self._searcher.print_junk()

    @staticmethod
    def _show_menu() -> None:
        ut.print_("\nMenu:")
        ut.print_("\tenter 's' - search junk files and directories;")
        ut.print_("\tenter 'a' - remove all found junk files and directories at once;")
        ut.print_("\tenter 'o' - remove found junk files and directories one by one;")
        ut.print_("\tenter 'q' - exit")

    def run(self, dir_path: Optional[str] = None) -> None:
        """
        :param dir_path: directory in which to search for junk.
        """

        if dir_path is not None:
            self._search_junk(dir_path)
        while True:
            self._show_menu()
            if self._get_task():
                return
