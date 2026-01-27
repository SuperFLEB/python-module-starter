#!/usr/bin/env python3
import os
import subprocess as sp
import re
import sys
from typing import Iterable

BUMPS = ["major", "minor", "patch"]
LABELS = ["pre", "alpha", "beta", "rc"]

def _split_version(string: str) -> tuple[int, int, int, str | None] | None:
    matches = re.match(r"^(\d+)\.(\d+)\.(\d+)(?:-(\S+))?$", string)
    if matches is None: return None
    groups = matches.groups()
    return int(groups[0]), int(groups[1]), int(groups[2]), groups[3]

def _get_version_from_tag() -> str | None:
    try:
        my_tag = sp.check_output(["git", "describe", "--tags", "--exact-match", "--match", "v*"], stderr=sp.DEVNULL).decode("utf-8").strip()
        return None if re.search(r"^v\d+\.\d+\.\d+$", my_tag) is None else my_tag[1:]
    except sp.CalledProcessError:
        return None

def _infer_version() -> str:
    # Use the exact tag if there is one
    try:
        my_tag = sp.check_output(["git", "describe", "--tags", "--exact-match", "--match", "v*"], stderr=sp.DEVNULL).decode("utf-8").strip()
        return my_tag[1:]
    except sp.CalledProcessError:
        pass

    # Use "major.minor.<patch+1>" if there is a prior version tag but not a current one
    try:
        raw_tag = sp.check_output(["git", "describe", "--tags", "--match", "v*"], stderr=sp.DEVNULL).decode("utf-8").strip()
        tag_parts = re.match(r"^v(\d+\.\d+)\.(\d+)-(\d+)-([a-z0-9]+)$", raw_tag)
        if tag_parts is not None:
            next_patch = int(tag_parts.group(2)) + 1
            return f"{tag_parts.group(1)}.{next_patch}"
    except sp.CalledProcessError:
        pass

    # Use "0.0.1" if there is no prior version tag
    return "0.0.1"

def _get_hash() -> str:
    return sp.check_output(["git", "rev-parse", "--short", "HEAD"], stderr=sp.DEVNULL).decode("utf-8").strip() or "unknown"

def bump(current_version: str, bump_version: str | None, bump_label: str | None, tags: Iterable[str] = None) -> str:
    if bump_version is not None and bump_version not in BUMPS: raise ValueError(f"Unknown bump: {bump_version}")
    if bump_label is not None and bump_label not in LABELS: raise ValueError(f"Unknown label: {bump_label}")

    other_versions = [t[1:] if t.startswith("v") else t for t in tags or []] or []

    parts = _split_version(current_version)

    next_patch: int = 0
    match bump_version:
        case "major":
            parts = [parts[0] + 1, 0, 0, None]
            next_patch = 0
        case "minor":
            parts = [parts[0], parts[1] + 1, 0, None]
            next_patch = 0
        case "patch":
            parts = [parts[0], parts[1], parts[2] + 1, None]
            next_patch = parts[2]
        case _:
            next_patch = parts[2] if parts[3] is not None else parts[2] + 1

    if bump_label is None:
        version_string = ".".join(map(str, parts[0:3]))
        if version_string in other_versions: raise ValueError(f"Version {version_string} already exists")
        return version_string

    next_sub = 1

    for tag in other_versions + [current_version]:
        sub_match = re.match(rf"{parts[0]}\.{parts[1]}\.{parts[2]}-{bump_label}(\d+)", tag)
        if sub_match is not None: next_sub = max(int(sub_match.group(1)) + 1, next_sub)
    return f"{parts[0]}.{parts[1]}.{next_patch}-{bump_label}{next_sub}"

def get_version() -> str:
    version = os.environ.get("BUILD_VERSION")
    if version is not None and re.search(r"^\d+\.\d+\.\d+(-\S+)?", version): return version
    version = _get_version_from_tag()
    if version is not None: return version
    return _infer_version()

def tag_version(version: str) -> None:
    if version is None or version == "":
        raise ValueError("Version tag cannot be empty")
    sp.check_call(["git", "tag", f"v{version}"], stderr=sp.DEVNULL)


def _cli() -> None:
    version = get_version()
    if "bump" in sys.argv:
        bump_version = [arg for arg in sys.argv if arg in BUMPS]
        bump_version = bump_version[0] if len(bump_version) > 0 else None

        label_bump = [arg for arg in sys.argv if arg in LABELS]
        label_bump = label_bump[0] if len(label_bump) > 0 else None

        tags = sp.check_output(["git", "tag", "--list", "v*"], stderr=sp.DEVNULL).decode("utf-8").strip().split("\n")

        if bump_version is None and label_bump is None:
            # This is a legitimate case if they just specify bumping "none" and "none", but only if the version doesn't exist
            if f"v{version}" in tags: raise ValueError(f"Version {version} already exists and nothing was bumped")
            print(version)
            exit(0)
        if bump_version is not None:
            print(bump(version, bump_version, label_bump, tags))
            exit(0)
    print(version)
    exit(0)

if __name__ == "__main__":
    _cli()