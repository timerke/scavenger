import os
import re


class Pattern:

    def __init__(self, pattern_re, pattern_str: str, dir_only: bool) -> None:
        """
        :param pattern_re: regex pattern;
        :param pattern_str:
        :param dir_only: if true, then pattern should only be applied to directories.
        """

        self._dir_only: bool = dir_only
        self._pattern_re = pattern_re
        self._pattern_str: str = pattern_str

    def __repr__(self) -> str:
        return self._pattern_str

    @classmethod
    def analyze_line(cls, pattern_str: str) -> "Pattern":
        """
        :param pattern_str: pattern format in string.
        :return: created pattern object.
        """

        initial_pattern = pattern_str
        pattern_str = pattern_str.replace(".", "\.")
        pattern_str = pattern_str.replace("*", ".*")
        dir_only = pattern_str.endswith("/")
        if dir_only:
            pattern_str = pattern_str[:-1]
        pattern_str = f"{pattern_str}$"
        pattern_re = re.compile(pattern_str)
        return Pattern(pattern_re, initial_pattern, dir_only)

    def match(self, path: str) -> bool:
        """
        :param path: path to check for consistency.
        :return: True if path matches pattern.
        """

        result = os.path.isdir(path) if self._dir_only else True
        base_name = os.path.basename(path)
        return result and bool(self._pattern_re.match(path)) or bool(self._pattern_re.match(base_name))
