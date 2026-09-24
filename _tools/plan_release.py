#!/usr/bin/env python3
"""Validate a committed release request and print the exact publication inputs.

Ported from Code Rules' `cmd/plan-release`. A release request is one new or edited
`releases/v<semver>.md` file between two commits. The printed plan binds that file's
version and notes to the head commit, which is the commit the release tags.
An empty `tag` means the range requests no release.
"""

import argparse
import json
import re
import subprocess
import sys

NOTES_DIR = "releases"
SEMVER = re.compile(
    r"^v(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:-((?:0|[1-9]\d*|\d*[A-Za-z-][0-9A-Za-z-]*)(?:\.(?:0|[1-9]\d*|\d*[A-Za-z-][0-9A-Za-z-]*))*))?$"
)


class PlanError(Exception):
    pass


def parse(tag):
    """Return a sortable SemVer 2.0.0 precedence key, or None for a non-version tag."""
    match = SEMVER.match(tag)
    if not match:
        return None
    core = tuple(int(part) for part in match.groups()[:3])
    pre = match.group(4)
    if pre is None:
        # A release without a prerelease suffix sorts after all of its prereleases.
        return core, (1,)
    # Numeric identifiers sort before alphanumeric ones and compare numerically.
    ids = tuple((0, int(i), "") if i.isdigit() else (1, 0, i) for i in pre.split("."))
    return core, (0,) + ids


def is_notes_file(name):
    parts = name.split("/")
    return len(parts) == 2 and parts[0] == NOTES_DIR and parts[1].startswith("v") and parts[1].endswith(".md")


def read(source, base, head, first):
    def git(*args):
        result = subprocess.run(["git", *args], cwd=source, capture_output=True, text=True)
        if result.returncode != 0:
            raise PlanError(f"git {' '.join(args)}: {result.stderr.strip()}")
        return result.stdout

    def resolve(ref):
        return git("rev-parse", "--verify", "--end-of-options", ref + "^{commit}").strip()

    def is_ancestor(ancestor, descendant):
        return subprocess.run(
            ["git", "merge-base", "--is-ancestor", ancestor, descendant], cwd=source, capture_output=True
        ).returncode == 0

    empty = {"tags": [], "tag": "", "version": "", "commit": "", "previous": "", "notes": "", "prerelease": False}
    base, head = resolve(base), resolve(head)
    if not is_ancestor(base, head):
        raise PlanError("release base must be an ancestor of head")
    tags = git("tag", "--list", "v*").split()

    fields = git("diff", "--name-status", "-z", "--no-renames", base, head, "--", NOTES_DIR + "/").split("\0")
    requested = None
    for status, name in zip(fields[0::2], fields[1::2]):
        if not is_notes_file(name):
            continue
        tag = name.split("/")[1][: -len(".md")]
        if status != "A":
            # Published notes are history; correct later behavior in a new release.
            if tag in tags:
                raise PlanError(f"tagged release notes are immutable: {name}")
            if status == "D":
                continue
            if status != "M":
                raise PlanError(f"unsupported release note change: {name}")
        if requested:
            raise PlanError("submit one release notes file per change")
        requested = name
    if not requested:
        return empty

    tag = requested.split("/")[1][: -len(".md")]
    current = parse(tag)
    if current is None:
        raise PlanError(f"{requested}: name the file v<MAJOR>.<MINOR>.<PATCH>[-prerelease].md, without build metadata")
    notes = git("show", f"{head}:{requested}")
    if not notes.strip():
        raise PlanError("release notes must not be empty")

    # A new request must not strand an earlier one that never reached tagging.
    for name in git("ls-tree", "-r", "--name-only", "-z", head, "--", NOTES_DIR + "/").split("\0"):
        if name and name != requested and is_notes_file(name):
            pending = name.split("/")[1][: -len(".md")]
            if pending not in tags:
                raise PlanError(f"resolve untagged release request {name} before requesting {tag}")

    observed, previous, latest = [], "", None
    for existing in tags:
        other = parse(existing)
        if other is None:
            continue
        if existing == tag:
            # Retrying a publication is allowed only when the tag already marks this exact commit.
            if resolve("refs/tags/" + tag) != head:
                raise PlanError(f"tag {tag} already points to another commit")
            continue
        observed.append(existing)
        if current <= other:
            raise PlanError(f"{tag} must be newer than existing tag {existing}")
        if latest is None or other > latest:
            previous, latest = existing, other
    if not previous and tag != first:
        raise PlanError(f"the first release must be {first}")
    if previous and not is_ancestor("refs/tags/" + previous, head):
        raise PlanError(f"previous release {previous} must be an ancestor of {head}")

    return {
        "tags": sorted(observed),
        "tag": tag,
        "version": tag[1:],
        "commit": head,
        "previous": previous,
        "notes": notes,
        "prerelease": "-" in tag,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--base", required=True, help="Commit before the release request")
    parser.add_argument("--head", default="HEAD", help="Commit containing the approved notes")
    parser.add_argument("--first", default="v1.0.0", help="Version required when no release exists yet")
    parser.add_argument("--source", default=".", help="Repository to inspect")
    args = parser.parse_args()
    try:
        plan = read(args.source, args.base, args.head, args.first)
    except PlanError as error:
        print(error, file=sys.stderr)
        return 1
    json.dump(plan, sys.stdout)
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
