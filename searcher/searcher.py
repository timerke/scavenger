import os
import shutil
from typing import List, Optional, Tuple
from searcher import utils as ut
from searcher.configreader import ConfigReader


class Searcher:
    """
    Scavenger hunt class.
    """

    def __init__(self, verbose_mode: bool = False, config_exc: Optional[str] = None, config_junk: Optional[str] = None
                 ) -> None:
        """
        :param verbose_mode: if True, then searcher will display found junk in real mode;
        :param config_exc: path to configuration file with exceptions;
        :param config_junk: path to configuration file with junk.
        """

        self._dir_config: str = os.path.join(os.curdir, "config")
        self._exceptions: List[Tuple[str, Optional[str]]] = []
        self._exceptions_number: int = 0
        config_exc = config_exc or os.path.join(self._dir_config, "exceptions.txt")
        self._exceptions_reader: ConfigReader = ConfigReader(config_exc)
        self._junk: List[Tuple[str, Optional[str]]] = []
        self._junk_number: int = 0
        config_junk = config_junk or os.path.join(self._dir_config, "junk.txt")
        self._junk_reader: ConfigReader = ConfigReader(config_junk)
        self._verbose_mode: bool = verbose_mode

    @staticmethod
    def _print(files_and_dirs: List[Tuple[str, Optional[str]]], obj_name: str) -> None:
        if len(files_and_dirs) > 0:
            ut.print_(f"\nFound {obj_name.lower()} files and directories:")
            for file_or_dir, message in files_and_dirs:
                ut.print_(f"{file_or_dir}{message}")
        else:
            ut.print_(f"\n{obj_name.title()} files and directories not found")

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
            ut.print_(f"Scanned files and folders: {total_number}, junk: {self._junk_number}, exceptions: "
                      f"{self._exceptions_number}", same_place=True)
            files_and_dirs.append(obj_path)
            if os.path.isdir(obj_path) and not is_junk:
                try:
                    total_number = self._search(obj_path, files_and_dirs, total_number)
                except PermissionError:
                    ut.print_(f"Error: access denied to '{obj_path}'")
        return total_number

    def print_exceptions(self) -> None:
        self._print(self._exceptions, "exceptions")

    def print_junk(self) -> None:
        self._print(self._junk, "junk")

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
