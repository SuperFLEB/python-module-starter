import pathlib
import typing
import shutil

from .Config import Config, package_path

def readme(config: Config) -> str:
    dashed = "-".join(package_path(config))
    dotted = ".".join(package_path(config))
    byline = " | ".join([item for item in (config.author.name, config.author.email, config.project_urls.Homepage) if item])
    return \
f"""
# {dotted}
{config.project_urls.Homepage or ''}
{byline or ''}

{config.description or "This is a Python package that presumably does some things."}

## To install

```python
pip install {dashed}
```

## To use

```python
import {dotted}

# Then do... something. Nobody wrote this documentation yet. Lorem to the ipsum to the dolor sit amet.
```
"""

def license(config: Config) -> str:
    return f"(Insert license text for {config.license} here...)"

def gitignore(config: Config) -> str:
    with open(pathlib.Path(__file__).parent / "assets" / "template.gitignore", "r") as fh:
        return fh.read()

def copy_github(config: Config) -> None:
    source = (pathlib.Path(__file__).parent / "assets" / "copy" / ".github").resolve()
    shutil.copytree(source, ".github")

def copy_buildscript(config: Config) -> None:
    source = (pathlib.Path(__file__).parent / "assets" / "copy" / "buildscript").resolve()
    shutil.copytree(source, "buildscript")

_FILE_GENERATORS: dict[str, typing.Callable[[Config], str]] = {
    "README.md": readme,
    "LICENSE": license,
    ".gitignore": gitignore,
}

_DIRECTORY_GENERATORS: dict[str, typing.Callable[[Config], None]] = {
    ".github": copy_github,
    "buildscript": copy_buildscript,
}

def generate(config: Config) -> None:
    for file, generator in _FILE_GENERATORS.items():
        try:
            with open(file, "x") as fh:
                fh.write(generator(config))
        except Exception as e:
            print(f"Failed to generate file {file}: {e}")
            continue
        print(f"Generated file: {file}")

    for directory, generator in _DIRECTORY_GENERATORS.items():
        try:
            generator(config)
        except Exception as e:
            print(f"Failed to generate directory {directory}: {e}")
            continue
        print(f"Wrote directory: {directory}")
