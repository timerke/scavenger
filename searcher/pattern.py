import os
import re


class Pattern:

    def __init__(self, pattern_re, dir_only: bool) -> None:
        """
        :param pattern_re: regex pattern;
        :param dir_only: if true, then pattern should only be applied to directories.
        """

        self._dir_only: bool = dir_only
        self._pattern_re = pattern_re

    @classmethod
    def analyze_line(cls, pattern_str: str) -> "Pattern":
        """
        :param pattern_str: pattern format in string.
        :return: created pattern object.
        """

        pattern_str = pattern_str.replace(".", "\.")
        pattern_str = pattern_str.replace("*", ".*")
        dir_only = pattern_str.endswith("/")
        if dir_only:
            pattern_str = pattern_str[:-1]
        pattern_str = f"{pattern_str}$"
        pattern_re = re.compile(pattern_str)
        return Pattern(pattern_re, dir_only)

    def match(self, path: str) -> bool:
        """
        :param path: path to check for consistency.
        :return: True if path matches pattern.
        """

        result = os.path.isdir(path) if self._dir_only else True
        base_name = os.path.basename(path)
        return result and bool(self._pattern_re.match(base_name))
