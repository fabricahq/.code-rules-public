# Fabrica Public Rules Library agent guide

This repository is a [Code Rules](https://github.com/fabricahq/code-rules) library. The [README](README.md) explains what it contains and how to contribute.

## Rules

Write and revise rules with the [Code Rules rule rubric and template](https://code-rules.fabricahq.com/reference/rule-authoring/). When you add, remove, rename, or retitle a rule or group, update the README's rule count badge, group table, and rule lists to match. Before you push, run these from the repository root:

```sh
code-rules library check
uv run .github/scripts/check-readme.py
```

The **Check** workflow runs both on every pull request.

<!-- release-planner:begin v0.3.2 sha256:eab1df264ef5ac2d -->
## Releases

This repository publishes releases with [Release Planner](https://github.com/fabricahq/release-planner) v0.3.2. When asked to make a release, draft or revise release notes, or retry a failed release, print the release procedure and follow it:

```sh
release-planner guide
```

First check that `release-planner version` prints `v0.3.2`. If it doesn't, or `release-planner` isn't installed, install that version:

```sh
curl -fsSL https://raw.githubusercontent.com/fabricahq/release-planner/v0.3.2/install.sh | sh -s -- --version v0.3.2
```

Read `.release-planner/policy.md` first for this repository's release policy. You prepare the release pull request; the maintainer approves the release by merging it. Never tag, publish, or merge.
<!-- release-planner:end -->
