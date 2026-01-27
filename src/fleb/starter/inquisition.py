import pathlib
import re

from .Config import Config
from .defaults import get_defaults

_DEFAULTS = get_defaults()

cwd_name = pathlib.Path().resolve().name

def _test_basic(string: str = "") -> bool:
    return not re.search(r"[\"\n\r\t]$", string or "")

def _test_name(string: str = "") -> bool:
    return re.search("^[a-zA-Z][a-zA-Z0-9_-]*$", string or "") and not re.search("[-_]{2,}", string or "")

def _input(prompt: str, key: str, required: bool = False, default: str = "") -> str:
    default = _DEFAULTS.get(key, default)
    result = None
    while not result:
        if required:
            default_bug = f" [{default}]" if default else ""
        else:
            default_bug = f" [{default or '(none)'}]"
        result = input(f"{prompt}{default_bug}: ") or default or ""
        if not required and not result: return ""
        if result: return result
        print("We need this. Type something.")

def inquisition() -> Config:
    print("Let's make a Python package!")
    print("-" * 80)

    config = Config()

    config.namespace = None
    while config.namespace is None:
        config.namespace = _input("Namespace", "namespace")
        if config.namespace != "" and not _test_name(config.namespace):
            print("Invalid namespace. Try again.")
            config.namespace = None

    config.name = None
    while config.name is None:
        config.name = _input("Package name", "name", default=cwd_name, required=True)
        if not _test_name(config.name):
            print("Invalid name. Try again.")
            config.namespace = None

    config.full_name = f"{config.namespace}-{config.name}" if config.namespace else config.name

    config.description = None
    while config.description is None:
        config.description = _input("Description", "description", default="A python module")
        if not _test_basic(config.description):
            print("Invalid description. Try again.")
            config.description = None

    config.keywords = re.split(",\s*", _input("Keywords (comma-separated, optional)", "keywords", default=""))
    config.keywords = [ks for k in config.keywords if _test_name(ks := k.strip())]

    config.requires_python = None
    while config.requires_python is None:
        config.requires_python = _input("Requires Python", "requires_python")
        if not (config.requires_python == "" or _test_basic(config.requires_python)):
            print("Invalid requires-python. Try again.")
            config.requires_python = None

    config.license = None
    while config.license is None:
        config.license = _input("License", "license", default="LicenseRef-None")
        if not _test_basic(config.license):
            print("Invalid license spec. Try again.")
            config.license = None

    config.github_username = None
    while config.github_username is None:
        config.github_username = _input("GitHub username", "github_username", default="")
        if config.github_username == "" or \
            not re.search(r"^[a-zA-Z0-9-]{1,39}$", config.github_username) or \
            re.search(r"[-_]{2,}", config.github_username):
                print("Invalid GitHub username. Try again.")
                config.github_username = None

    config.github_repo = None
    if config.github_username != "":
        while config.github_repo is None:
            config.github_repo = _input("GitHub repository name", "github_repo", default=config.name)
            if config.github_repo != "" and not re.search(r"^[a-zA-Z0-9_-]{1,100}$", config.github_repo):
                print("Invalid GitHub repository name. Try again.")
                config.github_repo = None

    gh_url = f"https://github.com/{config.github_username}/{config.github_repo}" if config.github_username and config.github_repo else None

    project_urls = {
        "Homepage": gh_url,
        "Author": None,
        "Source": gh_url,
        "Issues": f"{gh_url}/issues" if gh_url else None,
    }

    for key in project_urls:
        default = project_urls[key]
        project_urls[key] = None
        while project_urls[key] is None:
            project_urls[key] = _input(f"Project {key} URL", key, default=default)
            if not (project_urls[key] == "" or _test_basic(project_urls[key])):
                print("Invalid URL. Try again.")
                project_urls[key] = None

    for key, url in project_urls.items():
        if url:
            setattr(config.project_urls, key, url)

    config.author.name = None
    while config.author.name is None:
        config.author.name = _input("Author name", "author_name")
        if config.author.name != "" and not _test_basic(config.author.name):
            print("Invalid author name. Try again.")
            config.author.name = None

    config.author.email = None
    while config.author.email is None:
        config.author.email = _input("Author email address", "author_email")
        if config.author.email != "" and not _test_basic(config.author.email):
            print("Invalid author email address. Try again.")
            config.author.email = None

    config.author.name = config.author.name or None
    config.author.email = config.author.email or None
    return config

if __name__ == "__main__":
    inquisition()
