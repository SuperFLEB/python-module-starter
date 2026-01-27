import os
import subprocess
import sys
import pathlib
from util.version import get_version, bump

base = pathlib.Path(__file__)

GH_REPO = os.environ.get('GITHUB_REPOSITORY')
GH_TOKEN = os.environ.get('GITHUB_TOKEN')
ACT = os.environ.get("ACT") is not None

EXPLICIT_VERSION = os.environ.get('EXPLICIT_VERSION') or None
VERSION_BUMP = os.environ.get('VERSION_BUMP') or None
LABEL_BUMP = os.environ.get('LABEL_BUMP') or None

VERSION_BUMP = None if VERSION_BUMP == "none" else VERSION_BUMP
LABEL_BUMP = None if LABEL_BUMP == "none" else LABEL_BUMP

def run(run_args: list[str], **kwargs):
    if ACT:
        print("DRY RUN>>" + " ".join(run_args), file=sys.stderr)
        return None
    return subprocess.run(run_args, **kwargs)

if EXPLICIT_VERSION is not None:
    # Use a null bump to check for version collision
    version = bump(EXPLICIT_VERSION, None, None)
else:
    tags = subprocess.run(["git", "tag", "--list", "v*"], capture_output=True, text=True).stdout.strip().split("\n")
    version = bump(get_version(), VERSION_BUMP, LABEL_BUMP, tags)

print(version)
