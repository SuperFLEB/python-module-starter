from .Config import Config, package_path
from pathlib import Path

def scaffold(config: Config, src: str = "src"):
    path = Path(f"{src}/" + "/".join(package_path(config)))
    path.mkdir(parents=True, exist_ok=True)
    path.joinpath("__init__.py").touch()
