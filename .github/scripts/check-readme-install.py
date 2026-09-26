#!/usr/bin/env python3
"""Check that the README's install command pins the release being made and selects every group.

Release Planner runs this on the release commit, which adds _releases/<version>.md,
so the newest notes file names the version about to be tagged. Between releases the
command intentionally pins the previous release, so pull request checks don't run this.
Run from the repository root.
"""

import re
import shlex
import sys
from pathlib import Path

COMMAND = "code-rules project add library"
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


def install_options():
    """Return the --groups and --ref values of the README's command that adds this library.

    Joins the command's continuation lines and splits it as the shell would, so comments
    and other commands in the same code block don't count.
    """
    lines = Path("README.md").read_text().splitlines()
    starts = [i for i, line in enumerate(lines) if line.strip().startswith(COMMAND)]
    if len(starts) != 1:
        sys.exit(f"README.md must contain exactly one `{COMMAND}` command")
    index = starts[0]
    command = lines[index].rstrip()
    while command.endswith("\\"):
        index += 1
        command = command[:-1] + lines[index].rstrip()

    options = {"--groups": [], "--ref": []}
    words = iter(shlex.split(command, comments=True))
    for word in words:
        name, equals, value = word.partition("=")
        if name in options:
            options[name].append(value if equals else next(words, ""))
    return options


def main():
    version = releasing_version()
    if version.group(4):
        print(f"{version.group(0)} is a prerelease; the README keeps pinning a stable release.")
        return

    options = install_options()
    errors = []
    refs = options["--ref"]
    if not refs:
        errors.append(f"add --ref {version.group(0)}")
    elif refs != [version.group(0)]:
        errors.append(f"pin --ref {version.group(0)}, not {' '.join(refs)}")

    selected = options["--groups"]
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
