import dotenv
import os

def get_defaults() -> dict[str, str]:
    dotenv.load_dotenv()
    defaults = {
        "namespace": os.getenv("PYPROJECT_INIT_NAMESPACE", None),
        "license": os.getenv("PYPROJECT_INIT_LICENSE", None),
        "github_username": os.getenv("PYPROJECT_INIT_GITHUB_USERNAME", None),
        "author_name": os.getenv("PYPROJECT_INIT_AUTHOR_NAME", None),
        "author_email": os.getenv("PYPROJECT_INIT_AUTHOR_EMAIL", None),
        "author_homepage": os.getenv("PYPROJECT_INIT_AUTHOR_HOMEPAGE", None),
    }

    return {k: v for k, v in defaults.items() if v}

