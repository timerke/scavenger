from searcher.pattern import Pattern


def test_pattern_empty_line() -> None:
    line = "   "
    pattern = Pattern.analyze_line(line)
    assert pattern is None

