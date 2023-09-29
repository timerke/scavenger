import os
import shutil
from typing import List, Optional, Tuple
from searcher import utils as ut
from searcher.configreader import ConfigReader


class Searcher:
    """
    Scavenger hunt class.
    """

    def __init__(self, verbose_mode: bool = False) -> None:
        """
        :param verbose_mode: if True, then searcher will display found junk in real mode.
        """

        self._dir_config: str = os.path.join(os.curdir, "config")
        self._exceptions: List[Tuple[str, Optional[str]]] = []
        self._exceptions_number: int = 0
        self._exceptions_reader: ConfigReader = ConfigReader(os.path.join(self._dir_config, "exceptions.txt"))
        self._junk: List[Tuple[str, Optional[str]]] = []
        self._junk_number: int = 0
        self._junk_reader: ConfigReader = ConfigReader(os.path.join(self._dir_config, "junk.txt"))
        self._verbose_mode: bool = verbose_mode

    def _search(self, dir_path: str, files_and_dirs: List[str], total_number: int) -> int:
        """
        :param dir_path: directory to search in;
        :param files_and_dirs: list in which to place found paths of files and directories;
        :param total_number: total number of files and directories found.
        :return: total number of files and directories found.
        """

        for obj_name in os.listdir(dir_path):
            obj_path = os.path.join(dir_path, obj_name)
            is_junk, pattern = self._junk_reader.match(obj_path)
            if is_junk:
                is_exception, exc_pattern = self._exceptions_reader.match(obj_path)
                if is_exception:
                    self._exceptions_number += 1
                    pattern = exc_pattern
                    obj_list = self._exceptions
                    obj_name = "Exception"
                else:
                    self._junk_number += 1
                    obj_list = self._junk
                    obj_name = "Junk"
                message = pattern.get_formatted_message()
                obj_list.append((obj_path, message))
                if self._verbose_mode:
                    ut.print_(f"{obj_name} found. Path: '{obj_path}', pattern: '{pattern}'{message}")

            total_number += 1
            ut.print_(f"Number of scanned files and folders: {total_number}, number of found junk: {self._junk_number}",
                      same_place=True)
            files_and_dirs.append(obj_path)
            if os.path.isdir(obj_path) and not is_junk:
                try:
                    total_number = self._search(obj_path, files_and_dirs, total_number)
                except PermissionError:
                    ut.print_(f"Error: access denied to '{obj_path}'")
        return total_number

    def print_junk(self) -> None:
        if len(self._junk) > 0:
            ut.print_("\nFound junk files and directories:")
            for file_or_dir, message in self._junk:
                ut.print_(f"{file_or_dir}{message}")
        else:
            ut.print_("\nJunk files and directories not found")

    @staticmethod
    def remove(obj_path: str) -> None:
        """
        :param obj_path: path to object to be deleted.
        """

        if os.path.exists(obj_path):
            if os.path.isdir(obj_path):
                shutil.rmtree(obj_path)
            else:
                os.remove(obj_path)
            ut.print_(f"'{obj_path}' removed")
        else:
            ut.print_(f"Error: no '{obj_path}'")

    def search_junk(self, dir_path: Optional[str] = None) -> List[Tuple[str, Optional[str]]]:
        """
        :param dir_path: directory to search in.
        :return: list with found junk files and directories.
        """

        files_and_dirs = []
        self._junk.clear()
        self._junk_number = 0
        if dir_path is None:
            dir_path = os.curdir
        try:
            self._search(dir_path, files_and_dirs, 0)
        except FileNotFoundError:
            ut.print_(f"Error: no directory '{dir_path}'")
        return self._junk.copy()
