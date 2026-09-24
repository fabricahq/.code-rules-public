# Releases

This document owns release policy and the agent procedure for Fabrica Public Rules Library. It follows the [Code Rules release process](https://github.com/fabricahq/code-rules/blob/main/_engineering/releasing.md), adapted for a rule library: there are no binaries to build, so a release is a version tag plus its approved notes.

Say **“let's release”** to an agent working in this repository. The agent prepares a release PR containing `releases/v<version>.md`. Edit that Markdown file in the PR, save your changes, then **merge the PR to approve publication**.

**The merged Markdown file becomes the GitHub release description verbatim, including your manual edits.** The PR description and review comments are separate review context. Saving an intermediate edit does not publish anything; after merge, the [release workflow](../.github/workflows/release.yml) validates the library, tags the merged commit, and publishes the release.

## Agent procedure

1. **Establish the range.** Fetch `main` and tags. List published releases, including prereleases, and resolve the most recent version's tag to a commit. Verify it is an ancestor of the intended `main` commit. A draft or a tag without a published release is unfinished work: inspect that attempt before preparing another. With no published releases, use `v1.0.0` and review the repository's full history plus its current rules.
2. **Account for all changes.** Read every commit since the previous released tag and its associated PR, including direct commits. Read the relevant rule diffs and group metadata. In the PR description, record the base tag, analyzed source SHA, and an inventory mapping every commit/PR to a release-note entry or a reason for omission. Account for reverts and superseded work. Tooling, CI, and README-only changes may belong only in the inventory.
3. **Choose the version.** Apply the policy below and explain the proposed increment in the PR description. Flag uncertainty instead of inventing compatibility guarantees.
4. **Draft the notes.** Create exactly one `releases/v<version>.md` file on a release branch. Its filename owns the version; its contents become the GitHub release body verbatim. Follow the editorial format below. For the initial release, describe the library as it stands rather than the sequence of migration commits.
5. **Validate and present.** Run `code-rules library check` and `python3 _tools/plan_release.py --base origin/main --head HEAD` after committing the notes. Open a PR titled `Release v<version>` and link directly to the Markdown file's GitHub editor. State that saving edits updates the draft and merging authorizes publication. Leave the PR for the maintainer; the agent does not merge it on the maintainer's behalf.
6. **Preserve edits and refresh the range.** When asked to revise the draft, fetch its branch and retain manual edits. If `main` advanced, account for the new commits, update the inventory and notes, and bring the release branch up to date before approval. Keep rule changes outside the release PR. Finish only when every change through the reviewed source is accounted for and CI is green.

**After the agent finishes, the maintainer merges the release PR to approve publication.** No separate publish action is needed. If a check fails, the release stays unpublished; follow [Retry a failed release](#retry-a-failed-release).

For a second agent reviewing the draft, provide the previous tag, analyzed SHA, release-note file, and inventory. Ask it to identify omitted rule changes, unsupported claims, missing migration instructions, and an incorrect version increment. It should report evidence and propose edits without replacing the maintainer's wording or publishing.

## Editorial format

Use the same headings as Code Rules releases, when they have content:

- `## ✨ New Features`: new rules and groups.
- `## ⬆️ Improvements`: clearer guidance, better examples, or broader coverage in existing rules.
- `## 🐛 Squashed Bugs`: corrected rules. Name the rule, what it previously told agents to do, and the corrected guidance.
- `## ⛓️‍💥 Breaking Changes`: removed or renamed rules and groups, and reversed obligations. Name the affected IDs and the `exclude` or `replace` entries importers must update. Also call out a breaking change near the start so readers cannot miss it.
- `## What's Changed`: linked PR/commit inventory for readers who want detail.
- `## New Contributors`: only verified first contributions, with credit.

Give significant changes a descriptive `###` heading and a short explanation of why the change matters. Use bullets for small changes, code for commands, and before/after examples when they make an upgrade clearer. Omit empty categories. Group related commits into one coherent entry. Preserve the human's final wording.

End subsequent releases with one **Full Changelog** link using the actual previous and new tags. For `v1.0.0`, link to the tagged source and say it is the first release. Check all links.

## Version policy

Use [SemVer 2.0.0](https://semver.org/) with Git tags `vMAJOR.MINOR.PATCH`. Use a suffix such as `v1.1.0-rc.1` for prereleases; the workflow marks them as prereleases on GitHub. Omit build metadata from release tags.

The public contract is what importing projects reference: group IDs, rule IDs (their paths), and each rule's obligation. Projects name group IDs in `groups` and rule IDs in `exclude` and `replace`, and Code Rules rejects configuration that names a missing rule.

- Start at `v1.0.0`.
- Increment **major** to remove or rename a group or rule, or to reverse or substantially change what a rule obliges.
- Increment **minor** to add rules or groups, or to extend an existing rule to situations it did not cover.
- Increment **patch** for corrections, clarified wording, better examples, metadata, and attribution fixes that do not change what compliant code looks like.
- Each requested version must be newer than existing version tags. Publish one release before requesting the next.
- Published versions and tagged request files are immutable. Correct later behavior in a new release. If only published prose needs correction, edit the GitHub release description deliberately.

## Publication policy

- Publish only the source and notes approved by merging the release PR. Do not substitute a newer `main` commit during publication or a retry.
- The workflow validates the approved commit with `code-rules library check` before it creates the tag. It publishes last and verifies that the tag points to the approved commit.
- The workflow pins the Code Rules validator to a reviewed commit. Update that pin in a normal PR when the library format changes, and switch it to a released version once Code Rules publishes releases.
- Configure the `release` environment to allow only the `main` branch, with no reviewers or wait timers. Require pull requests for changes to `main` and protect its history from deletion and force pushes. Enable immutable releases so published tags cannot be moved.

## Retry a failed release

Prefer **Re-run all jobs** on the original failed Release run. To start a manual retry, use **Actions → Release → Run workflow**, select `main`, and copy both **Base SHA** and **Approved head SHA** from the original run summary into the corresponding inputs. Never substitute the latest `main` or guess the base from the head's parent.

Inspect the failed run and any existing tag or release before taking corrective action. If validation failed before tagging, correct the rules in a separate PR, then edit the untagged notes file in a new release PR; merging those corrected notes approves the new commit. You can also withdraw an untagged request by deleting its notes file. If a tag or draft already exists, inspect and explicitly resolve that attempt first; never move a published tag.

## Release tooling

- [`_tools/plan_release.py`](../_tools/plan_release.py) validates a release request and prints the version, commit, and notes to publish. It is a port of Code Rules' `plan-release`, with the first version set to `v1.0.0`.
- Test it with `python3 -m unittest discover -s _tools`.
