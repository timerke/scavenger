import os
import shutil
from typing import List, Optional
from searcher import utils as ut
from searcher.configreader import ConfigReader


class Searcher:

    def __init__(self) -> None:
        self._junk: List[str] = []
        self._junk_reader: ConfigReader = ConfigReader(os.path.join(os.curdir, "config", "junk.txt"))

    @staticmethod
    def _remove(obj_path: str) -> None:
        if os.path.exists(obj_path):
            if os.path.isdir(obj_path):
                shutil.rmtree(obj_path)
            else:
                os.remove(obj_path)
            ut.print_(f"'{obj_path}' removed")

    def _search(self, dir_path: str, files_and_dirs: List[str]) -> None:
        """
        :param dir_path: directory to search in;
        :param files_and_dirs: list in which to place found paths of files and directories.
        """

        for obj_name in os.listdir(dir_path):
            obj_path = os.path.join(dir_path, obj_name)
            is_junk = self._junk_reader.match(obj_path)
            if is_junk:
                self._junk.append(obj_path)
                ut.print_(f"Junk found: '{obj_path}'")
            files_and_dirs.append(obj_path)
            if os.path.isdir(obj_path) and not is_junk:
                try:
                    self._search(obj_path, files_and_dirs)
                except PermissionError:
                    ut.print_(f"Access denied to '{obj_path}'")

    def print_junk(self) -> None:
        ut.print_("\nFound junk files and directories:")
        for file_or_dir in self._junk:
            ut.print_(file_or_dir)

    def remove_junk(self, junk: Optional[List[str]] = None) -> None:
        if junk is None:
            junk = self._junk.copy()
        for file_or_dir in junk:
            try:
                self._remove(file_or_dir)
            except Exception:
                ut.print_(f"Failed to remove '{file_or_dir}'")

    def search_junk(self, dir_path: str = os.curdir) -> None:
        """
        :param dir_path: directory to search in.
        """

        files_and_dirs = []
        self._junk.clear()
        self._search(dir_path, files_and_dirs)