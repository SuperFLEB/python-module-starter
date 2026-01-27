from .Config import Config


def generate_contents(config: Config):
    return {k: v for k, v in ({
        "NAMESPACE": config.namespace,
        "LICENSE": config.license,
        "GITHUB_USERNAME": config.github_username,
        "AUTHOR_NAME": config.author.name,
        "AUTHOR_EMAIL": config.author.email,
        "AUTHOR_HOMEPAGE": config.project_urls.Author,
    }).items() if v}


def generate(config: Config, out_path: str = ".env.my_info"):
    contents = generate_contents(config)
    with open(".env.my_info", "x") as env_my_info_fh:
        env_my_info_fh.write(
            "# This .env file is used by the Python Starter Kit\n# Put it above the root of all your projects to stop answering the same questions every time.\n" + \
            "\n".join(f"PYPROJECT_INIT_{k}=\"{v}\"" for k, v in contents.items())
        )
