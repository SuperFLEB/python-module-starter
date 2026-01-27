import pathlib
import tomlkit
import dataclasses

from .Config import Config, package_path

ASSETS = pathlib.Path(__file__).parent / "assets"

def generate_overlay(config: Config):
    author: dict = dataclasses.asdict(config.author) if config.author else {}
    overlay = {
        "name": f"{config.namespace}-{config.name}" if config.namespace else config.name,
        "description": config.description,
        "keywords": config.keywords,
        "requires-python": config.requires_python,
        "license": config.license,
        "urls": dataclasses.asdict(config.project_urls),
        "authors": []
    }
    overlay["urls"] = {k: v for k, v in overlay["urls"].items() if v}
    overlay["authors"] = [{k: v for k, v in author.items() if v}]
    overlay = {k: v for k, v in overlay.items() if v}
    return overlay


def generate(config: Config, out_path: str = "pyproject.toml"):

    with open(ASSETS / "template.pyproject.toml", "r") as template_fh:
        pyproject_template = tomlkit.load(template_fh)
        pyproject_template["project"].update(generate_overlay(config))

    dotted = ".".join(package_path(config))
    pyproject_template["project"]["name"].comment(f"PyPI package name. Import using `import {dotted}`")

    with open(out_path, "x") as pyproject_fh:
        tomlkit.dump(pyproject_template, pyproject_fh)

def can_generate(out_path: str = "pyproject.toml"):
    return not pathlib.Path(out_path).exists()

