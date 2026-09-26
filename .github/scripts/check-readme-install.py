#!/usr/bin/env python3
"""Check that the README's install command pins the release being made and selects every group.

Release Planner runs this on the release commit, which adds _releases/<version>.md,
so the newest notes file names the version about to be tagged. Between releases the
command intentionally pins the previous release, so pull request checks don't run this.
Run from the repository root.
"""

import re
import sys
from pathlib import Path

GROUP_ROOTS = ("practices", "techs")
VERSION = re.compile(r"v(\d+)\.(\d+)\.(\d+)(?:-([0-9A-Za-z.-]+))?")


def precedence(match):
    """Order versions by SemVer; a prerelease sorts before its release."""
    major, minor, patch, prerelease = match.groups()
    identifiers = []
    for part in (prerelease or "").split("."):
        identifiers.append((0, int(part), "") if part.isdigit() else (1, 0, part))
    return (int(major), int(minor), int(patch), prerelease is None, identifiers)


def releasing_version():
    versions = [
        match for path in Path("_releases").glob("v*.md") if (match := VERSION.fullmatch(path.stem))
    ]
    if not versions:
        sys.exit("no release notes found in _releases/")
    return max(versions, key=precedence)


def install_command():
    """Return the README code block that adds this library."""
    for block in re.findall(r"```sh\n(.*?)```", Path("README.md").read_text(), re.DOTALL):
        if "code-rules project add library" in block:
            return block
    sys.exit("README.md has no `code-rules project add library` command")


def main():
    version = releasing_version()
    if version.group(4):
        print(f"{version.group(0)} is a prerelease; the README keeps pinning a stable release.")
        return

    command = install_command()
    errors = []
    refs = re.findall(r"--ref (\S+)", command)
    if refs != [version.group(0)]:
        errors.append(f"pin --ref {version.group(0)}, not {' '.join(refs) or 'nothing'}")

    selected = re.findall(r"--groups (\S+)", command)
    groups = [
        metadata.parent.as_posix()
        for root in GROUP_ROOTS
        for metadata in sorted(Path(root).glob("*/_group.yaml"))
    ]
    for group in groups:
        if group not in selected:
            errors.append(f"add --groups {group}")
    for group in selected:
        if group not in groups:
            errors.append(f"remove --groups {group}, which is not a group")
    if selected != sorted(selected):
        errors.append("list --groups in alphabetical order")

    if errors:
        print(
            f"The README's install command must select every group in {version.group(0)}:",
            file=sys.stderr,
        )
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        sys.exit(1)
    print(f"The README's install command selects all {len(groups)} groups in {version.group(0)}.")


if __name__ == "__main__":
    main()
