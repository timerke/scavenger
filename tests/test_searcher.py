import os
from searcher import Searcher


def test_search_junk() -> None:
    config_exc = os.path.join("tests", "exceptions.txt")
    config_junk = os.path.join("tests", "junk.txt")
    searcher = Searcher(config_exc=config_exc, config_junk=config_junk)
    junk = searcher.search_junk(os.path.join("tests", "dir_1"))
    assert len(junk) == 3
