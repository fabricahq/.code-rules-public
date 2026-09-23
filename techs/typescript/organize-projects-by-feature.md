---
title: "Organize Projects by Feature"
whenToRead: "Before designing or reorganizing a TypeScript application or monorepo around features and shared code."
impact: "LOW"
impactDescription: "keeps app and package trees grouped by product features rather than technical buckets alone"
tags: "typescript, project-structure, feature-folders, organization"

attribution:
  - url: "https://github.com/mkosir/typescript-style-guide/blob/86bebd58a987e23277dba02028c0ee2d6ffb5073/website/src/pages/index.mdx"
    description: "Underlying TypeScript Style Guide material; required notice is retained in NOTICE.md."
---

## Organize Projects by Feature

Example frontend monorepo project, where every application has file/folder grouped by feature:

```shell
apps/
|- product-manager/
|  |- common/
|  |  |- components/
|  |  |  |- Button/
|  |  |  |- ProductTitle/
|  |  |  |- ...
|  |  |  `- index.tsx
|  |  |- consts/
|  |  |  |- paths.ts
|  |  |  `- ...
|  |  |- hooks/
|  |  `- types/
|  |- modules/
|  |  |- HomePage/
|  |  |- ProductAddPage/
|  |  |- ProductPage/
|  |  |- ProductsPage/
|  |  |  |- api/
|  |  |  |  `- useGetProducts/
|  |  |  |- components/
|  |  |  |  |- ProductItem/
|  |  |  |  |- ProductsStatistics/
|  |  |  |  `- ...
|  |  |  |- utils/
|  |  |  |  `- filterProductsByType/
|  |  |  `- index.tsx
|  |  |- ...
|  |  `- index.tsx
|  |- eslint.config.mjs
|  |- package.json
|  `- tsconfig.json
|- warehouse/
|- admin-dashboard/
`- ...
```

- `modules` folder is responsible for implementation of each individual page, where all custom features for that page are being implemented (components, hooks, utils functions etc.).
- `common` folder is responsible for implementations that are truly used across application. Since it's a "global folder" it should be used sparingly.
  If same component e.g. `common/components/ProductTitle` starts being used on more than one page, it shall be moved to common folder.

In case using frontend framework with file-system based router (e.g. Nextjs), `pages` folder serves only as a router, where its responsibility is to define routes (no business logic implementation).

Example backend project structure with file/folder grouped by feature:

```shell
product-manager/
|- dist/
|-- database/
|   |-- migrations/
|   |   |-- 20220102063048_create_accounts.ts
|   |   `-- ...
|   `-- seeders/
|       |-- 20221116042655-feeds.ts
|       `-- ...
|- docker/
|- logs/
|- scripts/
|- src/
|  |- common/
|  |  |- consts/
|  |  |- middleware/
|  |  |- types/
|  |  `- ...
|  |- dao/
|  |  |- user/
|  |  `- ...
|  |- modules/
|  |   |-- admin/
|  |   |   |-- account/
|  |   |   |   |-- account.model.ts
|  |   |   |   |-- account.controller.ts
|  |   |   |   |-- account.route.ts
|  |   |   |   |-- account.service.ts
|  |   |   |   |-- account.validation.ts
|  |   |   |   |-- account.test.ts
|  |   |   |   `-- index.ts
|  |   |   `-- ...
|  |   |-- general/
|  |   |   |-- general.model.ts
|  |   |   |-- general.controller.ts
|  |   |   |-- general.route.ts
|  |   |   |-- general.service.ts
|  |   |   |-- general.validation.ts
|  |   |   |-- general.test.ts
|  |   |   `-- index.ts
|  |   |- ...
|  |   `- index.tsx
|  `- ...
|- ...
|- eslint.config.mjs
|- package.json
`- tsconfig.json
```
