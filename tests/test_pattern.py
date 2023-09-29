import os
from searcher.pattern import Pattern


def test_message_for_pattern() -> None:
    line = "pattern | Message for pattern"
    pattern = Pattern.analyze_line(line)
    assert pattern is not None
    assert pattern.message == "Message for pattern"
    assert pattern.match("pattern")
    assert not pattern.match("some_pattern")

    line = "pattern"
    pattern = Pattern.analyze_line(line)
    assert pattern is not None
    assert pattern.message is None
    assert pattern.match("pattern")
    assert not pattern.match("some_pattern")


def test_pattern_asterisk() -> None:
    line = "some_*_pattern"
    pattern = Pattern.analyze_line(line)
    assert pattern is not None
    assert pattern.match(os.path.join("dir_1", "dir_2", "some__pattern"))
    assert pattern.match(os.path.join("dir_1", "dir_2", "some_another_pattern"))
    assert not pattern.match(os.path.join("dir_1", "dir_2", "some_pattern"))


def test_pattern_backslash_before_hashtag() -> None:
    line = "\#some_path"
    pattern = Pattern.analyze_line(line)
    assert pattern is not None
    assert pattern.match("#some_path")
    assert pattern.match(os.path.join("dir_1", "dir_2", "#some_path"))
    assert not pattern.match("some_path")


def test_pattern_comment() -> None:
    line = "# This is some kind of comment"
    pattern = Pattern.analyze_line(line)
    assert pattern is None


def test_pattern_dir_only() -> None:
    line = "dir_2/"
    pattern = Pattern.analyze_line(line)
    assert pattern is not None
    assert pattern.match(os.path.join("tests", "dir_1", "dir_2"))

    line = "dir_1/file/"
    pattern = Pattern.analyze_line(line)
    assert pattern is not None
    assert not pattern.match(os.path.join("tests", "dir_1", "file"))


def test_pattern_empty_line() -> None:
    line = "   "
    pattern = Pattern.analyze_line(line)
    assert pattern is None


def test_pattern_plus_symbol() -> None:
    line = "some_+_pattern"
    pattern = Pattern.analyze_line(line)
    assert pattern is not None
    assert pattern.match(os.path.join("dir_1", "dir_2", "some_h_pattern"))
    assert pattern.match(os.path.join("dir_1", "dir_2", "some_haha_pattern"))
    assert not pattern.match(os.path.join("dir_1", "dir_2", "some__pattern"))
    assert not pattern.match(os.path.join("dir_1", "dir_2", "some_pattern"))


def test_pattern_question_symbol() -> None:
    line = "some_?_pattern"
    pattern = Pattern.analyze_line(line)
    assert pattern is not None
    assert pattern.match(os.path.join("dir_1", "dir_2", "some__pattern"))
    assert pattern.match(os.path.join("dir_1", "dir_2", "some_1_pattern"))
    assert not pattern.match(os.path.join("dir_1", "dir_2", "some_12_pattern"))
    assert not pattern.match(os.path.join("dir_1", "dir_2", "some_pattern"))


def test_pattern_slash() -> None:
    line = "dir_1/dir_2/file"
    pattern = Pattern.analyze_line(line)
    assert pattern is not None
    assert pattern.match(os.path.join("dir_1", "dir_2", "file"))
    assert not pattern.match("dir/dir_0/dir_1/dir_2/file")
    assert not pattern.match("dir2/file")


def test_pattern_square_brackets() -> None:
    line = "som[ae]pattern"
    pattern = Pattern.analyze_line(line)
    assert pattern is not None
    assert pattern.match(os.path.join("dir_1", "dir_2", "somepattern"))
    assert pattern.match(os.path.join("dir_1", "dir_2", "somapattern"))
    assert not pattern.match(os.path.join("dir_1", "dir_2", "somipattern"))
    assert not pattern.match(os.path.join("dir_1", "dir_2", "sompattern"))
    assert not pattern.match(os.path.join("dir_1", "dir_2", "somApattern"))

    line = "som[a-z]pattern"
    pattern = Pattern.analyze_line(line)
    assert pattern is not None
    assert pattern.match(os.path.join("dir_1", "dir_2", "somepattern"))
    assert pattern.match(os.path.join("dir_1", "dir_2", "somapattern"))
    assert pattern.match(os.path.join("dir_1", "dir_2", "somipattern"))
    assert not pattern.match(os.path.join("dir_1", "dir_2", "sompattern"))
    assert not pattern.match(os.path.join("dir_1", "dir_2", "somApattern"))
