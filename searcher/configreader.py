import os
from typing import List
from searcher import utils as ut
from searcher.pattern import Pattern


class ConfigReader:

    def __init__(self, config_path: str) -> None:
        """
        :param config_path: path to configuration file.
        """

        self._config_path: str = config_path
        self._patterns: List[Pattern] = []
        self._init()

    def _analyze_content(self, lines: List[str]) -> None:
        """
        :param lines:
        """

        for line in lines:
            line = line.strip()
            if not line.startswith("#") and line:
                pattern = Pattern.analyze_line(line)
                self._patterns.append(pattern)

    def _init(self) -> None:
        if os.path.exists(self._config_path):
            lines = self._read_config()
            self._analyze_content(lines)
        else:
            ut.print_(f"No configuration file '{self._config_path}'")

    def _read_config(self) -> List[str]:
        """
        :return: lines from configuration file.
        """

        try:
            with open(self._config_path, "r", encoding="utf-8") as file:
                lines = file.read().split("\n")
        except Exception as exc:
            lines = []
            ut.print_(f"Failed to read configuration file '{self._config_path}' ({exc})")
        return lines

    def match(self, path: str) -> bool:
        for pattern in self._patterns:
            if pattern.match(path):
                return True
        return False
