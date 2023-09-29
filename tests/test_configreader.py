import os
from searcher.configreader import ConfigReader


def test_match() -> None:
    config_path = os.path.join("tests", "junk.txt")
    reader = ConfigReader(config_path)

    assert reader.match(os.path.join("dir", "some_file.pyc"))[0]
    assert reader.match(os.path.join("dir", "other_file.pyo"))[0]
    assert not reader.match(os.path.join("dir", "other_file.py"))[0]
    assert reader.match(os.path.join("dir", "som_pattern"))[0]
    assert reader.match(os.path.join("dir", "some_pattern"))[0]
    assert not reader.match(os.path.join("dir", "sompattern"))[0]


def test_match_with_incorrect_config_path() -> None:
    config_path = os.path.join("tests", "false_path.txt")
    reader = ConfigReader(config_path)

    assert not reader.match(os.path.join("dir", "some_file.pyc"))[0]
    assert not reader.match(os.path.join("dir", "other_file.pyo"))[0]
    assert not reader.match(os.path.join("dir", "other_file.py"))[0]
    assert not reader.match(os.path.join("dir", "som_pattern"))[0]
    assert not reader.match(os.path.join("dir", "some_pattern"))[0]
    assert not reader.match(os.path.join("dir", "sompattern"))[0]
