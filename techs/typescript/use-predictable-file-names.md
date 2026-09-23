---
title: "Use Predictable File Names"
whenToRead: "Before adding or renaming TypeScript source files, components, tests, or stories."
impact: "LOW"
impactDescription: "makes file paths searchable and keeps filename exceptions explicit"
tags: "typescript, frontend, file-names, naming, kebab-case, routes"
---

## Use Predictable File Names

Frontend source file names must make the file's scope predictable from the path.
Use lowercase kebab-case for authored source files, and add only narrow,
well-known dot suffixes before the extension.

**Incorrect:**

```txt
ItemExplorer.tsx
itemExplorer.tsx
index.tsx
query_keys.test.ts
```

**Correct:**

```txt
item-explorer.tsx
item-explorer.test.tsx
query-keys.test.ts
contracts.check.generated.ts
```

**Guidelines:**

- Use lowercase kebab-case for normal source files: `item-explorer.tsx`,
  `use-click-outside.ts`, `template-tree-store.ts`.
- Name a component file after the UI concept it owns rather than hiding it behind
  `index.tsx`. Route files and documented package entry points are the exceptions.
- Use `.tsx` only when the file contains JSX. Hooks, stores, mappers, and helpers
  stay `.ts` unless they render or return JSX.
- Use dot suffixes only for file roles that are already part of the project:
  `.test`, `.mock`, `.generated`, `.gen`, `.check`, `.config`, and `.d`.
- Keep TanStack Router's required route filenames as framework exceptions:
  `route.tsx`, `index.tsx`, `__root.tsx`, and dynamic `$param.tsx` files.
- Treat generated files and vendored/public assets as tool-owned exceptions; do
  not rename them to satisfy authored-source conventions.
- Run the project's filename lint check after adding or renaming source files.
  Keep its exception list aligned with framework and generated-file needs.

Reference: [bulletproof-react project standards](https://github.com/alan2207/bulletproof-react/blob/master/docs/project-standards.md#file-naming-conventions)
