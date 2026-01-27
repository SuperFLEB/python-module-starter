import pathlib

# This is probably awful. I made it late at night and couldn't quite rub the brain cells together.
# It does work though... so ship it!

def _subtree(path: pathlib.Path = None, parents_last: list[bool] = None, output: str = "") -> str:
    path = path or pathlib.Path(".")
    parents_last = parents_last or []

    dir_last = parents_last[-1] if parents_last else True

    pipes = "".join(["   " if pl else " │ " for pl in parents_last[:-1]])
    joint = "  └─" if dir_last else " ├─"

    if path.name:
        output += f"{pipes}{joint} ◲ {path.name}\n"

    files = []
    dirs = []

    for child in path.iterdir():
        (files if child.is_file() else dirs).append(child)

    for idx, d in enumerate(dirs):
        last = idx == len(dirs) - 1
        output = _subtree(d, parents_last + [last and not files], output)

    for idx, f in enumerate(files):
        last = idx == len(files) - 1
        if parents_last:
            last_pipe = "   " if dir_last else " │ "
        else:
            last_pipe = ""
        joint = " └─" if last else " ├─"
        output += f"{pipes}{last_pipe}{joint} ☰ {f.name}\n"
    return output

def tree(path: pathlib.Path = None) -> str:
    path = path or pathlib.Path(".")
    output = f" ◲ {path.name or '.'}\n"
    return _subtree(path, [], output)
