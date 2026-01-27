from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class Urls:
    Homepage: Optional[str] = None
    Author: Optional[str] = None
    Source: Optional[str] = None
    Issues: Optional[str] = None

@dataclass
class Author:
    name: Optional[str] = None
    email: Optional[str] = None


@dataclass
class Config:
    def __init__(self) -> None:
        self.project_urls = Urls()
        self.author = Author()
        self.keywords = []

    project_urls: Urls
    author: Optional[Author]
    keywords: list[str]

    namespace: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    requires_python: Optional[str] = None
    license: Optional[str] = None
    github_username: Optional[str] = None
    github_repo: Optional[str] = None

def package_path(config: Config) -> list[str]:
    return [part for part in (config.namespace or "").split("-") if part] + [config.name]
