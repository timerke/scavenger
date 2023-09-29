import os
import re
from typing import Optional
from searcher import utils as ut


class Pattern:

    def __init__(self, pattern_re, pattern_str: str, message: str, dir_only: bool) -> None:
        """
        :param pattern_re: regex pattern;
        :param pattern_str:
        :param message: message to display when pattern is matched;
        :param dir_only: if true, then pattern should only be applied to directories.
        """

        self._dir_only: bool = dir_only
        self._message: str = message
        self._pattern_re = pattern_re
        self._pattern_str: str = pattern_str

    def __repr__(self) -> str:
        return self._pattern_str

    @classmethod
    def _analyze_string_pattern(cls, pattern_str: str, message: Optional[str] = None) -> "Pattern":
        """
        :param pattern_str: pattern format in string;
        :param message: message to display when pattern is matched.
        :return: created pattern object.
        """

        initial_pattern = pattern_str
        pattern_str = pattern_str.replace(".", "\.")
        pattern_str = pattern_str.replace("*", ".*")
        pattern_str = pattern_str.replace("?", ".?")
        pattern_str = pattern_str.replace("+", ".+")
        dir_only = pattern_str.endswith("/")
        if dir_only:
            pattern_str = pattern_str[:-1]
        pattern_str = f"{pattern_str}$"
        pattern_re = re.compile(pattern_str)
        return Pattern(pattern_re, initial_pattern, message, dir_only)

    @classmethod
    def analyze_line(cls, line: str, config_path: Optional[str] = None) -> Optional["Pattern"]:
        """
        :param line: line from configuration file for which to create pattern;
        :param config_path: path to configuration file.
        :return: created pattern object.
        """

        line = line.strip()
        if line and not line.startswith("#"):
            line_parts = [part.strip() for part in line.split("|")]
            line_parts_number = len(line_parts)
            if line_parts_number > 2:
                config_message = f" '{config_path}'" if config_path else ""
                ut.print_(f"Error: line '{line}' from configuration file'{config_message}' will be ignored, format is "
                          f"incorrect")
                return None
            if line_parts_number == 1:
                pattern_str, message = line_parts[0], None
            else:
                pattern_str, message = line_parts
            return cls._analyze_string_pattern(pattern_str, message)
        return None

    def get_formatted_message(self) -> str:
        """
        :return: formatted message when pattern is matched.
        """

        return f" ({self._message})" if self._message else ""

    def match(self, path: str) -> bool:
        """
        :param path: path to check for consistency.
        :return: True if path matches pattern.
        """

        result = os.path.isdir(path) if self._dir_only else True
        base_name = os.path.basename(path)
        path = path.replace(os.sep, "/")
        return result and bool(self._pattern_re.match(path)) or bool(self._pattern_re.match(base_name))
