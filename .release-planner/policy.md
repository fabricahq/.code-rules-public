# Release policy

Release Planner's agent reads this file before every release. Fabrica Public Rules Library is a [Code Rules](https://github.com/fabricahq/code-rules) rule library: a release is a version tag on the rules and their metadata. There are no binaries or packages to build.

## Breaking changes

Projects import this library by pinning a version with `--ref` and naming what they want in their Code Rules configuration: group IDs in `groups`, and rule IDs in `exclude` and `replace`. Code Rules rejects a configuration that names a group or rule the library doesn't have. A change is breaking when it forces an importing project to change that configuration, or when compliant code under the old rule is no longer compliant under the new one. That includes:

- Removing or renaming a group. A group's ID is its directory, such as `techs/react`, so moving or renaming the directory renames the group.
- Removing or renaming a rule. A rule's ID is its path within its group, such as `techs/react/server-auth-actions`, so renaming the file or moving it to another group renames the rule.
- Reversing what a rule obliges, or changing it substantially enough that code which followed the old rule now violates it.
- Library metadata in `rule-library.yaml` that Code Rules depends on to read the library, such as raising `formatVersion` so that older Code Rules versions can't read it.

These are not breaking:

- Adding rules or groups. Importers who select groups with a wildcard, such as `--groups '*'`, receive new groups automatically. That is how wildcards are documented to work, so it isn't breaking, but the notes must name each new group.
- Changing a group's `name`, `description`, or `whenToRead` in `_group.yaml`, or a rule's `title`, `whenToRead`, `impact`, `impactDescription`, or `tags`, as long as its ID and obligation are unchanged.
- Editing background material in `assets/`, as long as the rules that link to it still resolve.
- Changes to the README, release tooling, or CI.

## Choosing a version

Versions follow [SemVer 2.0.0](https://semver.org/), with tags such as `v1.2.3`. The first release is v1.0.0. Use a suffix such as `v1.1.0-rc.1` for a prerelease.

- **Major:** any breaking change above, such as removing or renaming a group or rule, or reversing or substantially changing what a rule obliges.
- **Minor:** a new group, a new rule in an existing group, a rule extended to situations it didn't cover before, or a deprecation.
- **Patch:** clearer wording, better examples, metadata, attribution, and corrections that don't change what compliant code looks like.

When one change could fit two levels, such as a correction that also narrows what a rule allows, choose the higher level and explain why in the pull request. Don't invent compatibility guarantees: if you can't tell whether code that followed the old rule still follows the new one, say so and ask.

## Who reads the release notes

Readers:

- Engineers who import this library into their projects with Code Rules, deciding whether to move their `--ref` to the new version and what, if anything, they must change in their configuration.
- People evaluating the library for the first time, who read the notes to learn what it covers.

They know Code Rules and their own stack. They don't know the history of this repository, so describe what each rule now tells agents to do, not how the rule was edited.

## Order of the release notes

The notes present changes in these sections, in this order, leaving out any with nothing to say:

1. New groups: groups added to the library. Importers who select groups with a wildcard receive them automatically.
2. New rules: rules added to existing groups. Importers who select a group receive its new rules automatically.
3. Rule improvements: clearer guidance, better examples, broader coverage, and metadata changes such as `whenToRead` that change when agents load a rule.
4. Rule fixes: rules that told agents something wrong, with the previous and corrected guidance.
5. Deprecations: rules and groups that a later major version will remove or rename, and what to use instead.
6. Compatibility: non-breaking changes to `rule-library.yaml`, or to the Code Rules versions that can read the library.
7. Breaking changes: removed or renamed rules and groups, reversed obligations, and library changes that older Code Rules versions can't read.

Breaking changes come last. A deprecation should precede the major release that removes or renames what it deprecates whenever possible.

## Always and never

- Always name affected rules and groups by their IDs, such as `techs/react/server-auth-actions`, as described in the release notes style.
- Always credit external contributors by GitHub handle.
- Always credit third-party sources when a release adds rules adapted from them, and keep [NOTICE.md](../NOTICE.md) accurate.
- For the first release, describe the library as it stands, not the sequence of commits that built it.
- Never list README, CI, or release tooling changes under the sections above. They belong only in Pull Requests.
- Never include rule changes in a release pull request. Merge them in their own pull requests first, then release.
- Always update the README's install command in the release pull request: pin `--ref` to the new version and select every group. List that commit under Pull Requests. The release check enforces this. It can't change earlier, because the command must work with the release it pins.
