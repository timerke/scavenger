from typing import Optional
from searcher import Searcher
from searcher import utils as ut


class Menu:

    def __init__(self) -> None:
        self._searcher: Searcher = Searcher()

    @staticmethod
    def _exit() -> int:
        return 1

    @staticmethod
    def _get_directory_to_search() -> str:
        ut.print_("In which directory to search junk (by default in current directory)?")
        dir_path = input()
        if not dir_path:
            dir_path = "."
        return dir_path

    def _get_task(self) -> None:
        tasks = {"s": self._search_junk,
                 "a": self._remove_all,
                 "o": self._remove_one_by_one,
                 "q": self._exit}
        while True:
            ut.print_("Your choice: ", end="")
            user_answer = input().lower()
            task = tasks.get(user_answer, None)
            if task is None:
                ut.print_("Unknown choice. Try again")
                continue
            return task()

    def _remove_all(self) -> None:
        ut.print_("Removing all found junk files and directories...")
        self._searcher.remove_junk()

    def _remove_one_by_one(self) -> None:
        pass

    def _search_junk(self, dir_path: Optional[str] = None) -> None:
        if dir_path is None:
            dir_path = self._get_directory_to_search()
        ut.print_(f"Searching for junk in directory '{dir_path}'...")
        self._searcher.search_junk(dir_path)

    @staticmethod
    def _show_menu() -> None:
        ut.print_("Menu:")
        ut.print_("\tenter 's' - search junk files and directories;")
        ut.print_("\tenter 'a' - remove all found junk files and directories at once;")
        ut.print_("\tenter 'o' - remove found junk files and directories one by one;")
        ut.print_("\tenter 'q' - exit")

    def run(self, dir_path: Optional[str] = None) -> None:
        if dir_path is not None:
            self._search_junk(dir_path)
        while True:
            self._show_menu()
            if self._get_task():
                return
