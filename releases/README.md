# Release requests

The agent writes one `v<semver>.md` file here per release. The first is `v1.0.0.md`.

Edit the notes in the release PR, save your changes, and merge the PR to authorize publication. CI checks the approved commit with `code-rules library check`, tags it, and publishes the notes verbatim as the GitHub release.

Follow [the release procedure](../_engineering/releasing.md) for drafting, version selection, and retries.
