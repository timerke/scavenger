last_line_length = 0
same_line = False


def print_(string: str, **kwargs) -> None:
    global last_line_length, same_line

    if "same_place" in kwargs:
        print(f"{string}\r", flush=True, end="")
        last_line_length = len(string)
        same_line = True
    else:
        if same_line:
            print(" " * last_line_length, flush=True, end="\r")
        print(string, **kwargs, flush=True)
