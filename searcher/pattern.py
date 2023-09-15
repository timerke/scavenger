import os
import re


class Pattern:

    def __init__(self, pattern_re, dir_only: bool) -> None:
        self._dir_only: bool = dir_only
        self._pattern_re = pattern_re

    @classmethod
    def analyze_line(cls, pattern_str: str) -> "Pattern":
        pattern_str = pattern_str.replace(".", "\.")
        pattern_str = pattern_str.replace("*", ".*")
        dir_only = pattern_str.endswith("/")
        if dir_only:
            pattern_str = pattern_str[:-1]
        pattern_re = re.compile(pattern_str)
        return Pattern(pattern_re, dir_only)

    def match(self, path: str) -> bool:
        result = os.path.isdir(path) if self._dir_only else True
        base_name = os.path.basename(path)
        return result and bool(self._pattern_re.match(base_name))
