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
        ut.print_("\nExit")
        return 1

    @staticmethod
    def _get_directory_to_search() -> str:
        """
        :return: directory in which to search for junk.
        """

        ut.print_("In which directory to search junk (by default in current directory)?")
        ut.print_("Your answer: ", end="")
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
        user_answer = self._get_user_answer("s", "a", "o", "q")
        task = tasks.get(user_answer)
        if task is not None:
            return task()

    @staticmethod
    def _get_user_answer(*valid_answers) -> str:
        """
        :param valid_answers: list of valid user answers.
        :return: user answer.
        """

        valid_answers = [answer.lower() for answer in valid_answers]
        while True:
            ut.print_("Your answer: ", end="")
            user_answer = input().lower()
            if user_answer in valid_answers:
                return user_answer
            ut.print_("Unknown choice. Try again")

    def _get_yes_or_no_answer(self) -> bool:
        """
        :return: True if user's answer is yes.
        """

        return self._get_user_answer("y", "n") == "y"

    def _remove_all(self) -> None:
        ut.print_("\nRemoving all found junk files and directories...")
        self._remove_junk(False)

    def _remove_junk(self, ask_user: bool = True) -> None:
        """
        :param ask_user: if True, then need to ask user before deleting file or directory.
        """

        if self._junk:
            for file_or_dir in self._junk:
                if ask_user:
                    ut.print_(f"Remove '{file_or_dir}' (y/n)?")
                    answer = self._get_yes_or_no_answer()
                else:
                    answer = True

                if answer:
                    try:
                        self._searcher.remove(file_or_dir)
                    except Exception:
                        ut.print_(f"Error: failed to remove '{file_or_dir}'")
            self._junk.clear()
        else:
            ut.print_("No junk to remove")

    def _remove_one_by_one(self) -> None:
        ut.print_("\nRemoving found junk files and directories one by one...")
        self._remove_junk()

    def _search_junk(self, dir_path: Optional[str] = None) -> None:
        """
        :param dir_path: directory in which to search for junk.
        """

        if dir_path is None:
            dir_path = self._get_directory_to_search()
        ut.print_(f"\nSearching for junk in directory '{dir_path}'...")
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
