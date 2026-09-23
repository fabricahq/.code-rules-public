---
title: "Colocate Code by Feature"
whenToRead: "Before placing a TypeScript feature implementation, its tests, and related types in a project tree."
impact: "MEDIUM"
impactDescription: "keeps related implementation close to the feature that owns it"
tags: "typescript, organization, colocation, feature-folders, architecture"

attribution:
  - url: "https://github.com/mkosir/typescript-style-guide/blob/86bebd58a987e23277dba02028c0ee2d6ffb5073/website/src/pages/index.mdx"
    description: "Underlying TypeScript Style Guide material; required notice is retained in NOTICE.md."
---

## Colocate Code by Feature

- Every application or package in monorepo has project files/folders organized and grouped **by feature**.
- **Collocate code as close as possible to where it's relevant.**
- Deep folder nesting should not represent an issue.
