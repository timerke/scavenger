import os
from typing import List, Optional, Tuple
from searcher import utils as ut
from searcher.pattern import Pattern


class ConfigReader:
    """
    Class for reading configuration file.
    """

    def __init__(self, config_path: str) -> None:
        """
        :param config_path: path to configuration file.
        """

        self._config_path: str = config_path
        self._patterns: List[Pattern] = []
        self._init()

    def _analyze_content(self, lines: List[str]) -> None:
        """
        :param lines: lines from configuration file.
        """

        for line in lines:
            line = line.strip()
            if line and not line.startswith("#"):
                self._patterns.append(Pattern.analyze_line(line))

    def _init(self) -> None:
        if os.path.exists(self._config_path):
            self._analyze_content(self._read_config())
        else:
            ut.print_(f"Error: no configuration file '{self._config_path}'")

    def _read_config(self) -> List[str]:
        """
        :return: lines from configuration file.
        """

        try:
            with open(self._config_path, "r", encoding="utf-8") as file:
                lines = file.read().split("\n")
        except Exception as exc:
            lines = []
            error = f" ({exc})" if str(exc) else ""
            ut.print_(f"Error: failed to read configuration file '{self._config_path}'{error}")
        return lines

    def match(self, path: str) -> Tuple[bool, Optional[Pattern]]:
        """
        :param path: path to check if it matches configuration file.
        :return: True if path matches and pattern that path matches.
        """

        for pattern in self._patterns:
            if pattern.match(path):
                return True, pattern
        return False, None
