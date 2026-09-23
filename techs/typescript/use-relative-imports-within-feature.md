---
title: "Use Relative Imports Within a Feature"
whenToRead: "Before writing imports within a TypeScript feature or across feature boundaries."
impact: "LOW"
impactDescription: "keeps nearby feature imports movable while reserving absolute imports for shared or distant code"
tags: "typescript, imports, relative-imports, absolute-imports, organization"

attribution:
  - url: "https://github.com/mkosir/typescript-style-guide/blob/86bebd58a987e23277dba02028c0ee2d6ffb5073/website/src/pages/index.mdx"
    description: "Underlying TypeScript Style Guide material; required notice is retained in NOTICE.md."
---

## Use Relative Imports Within a Feature

Import paths can be relative, starting with `./` or `../`, or they can be absolute `@common/utils`.

To make import statements more readable and easier to understand:

- **Relative** imports `./sortItems` must be used when importing files within the same feature, that are 'close' to each other, which also allows moving feature around the codebase without introducing changes in these imports.
- **Absolute** imports `@common/utils` must be used in all other cases.
- **All** imports must be auto sorted by tooling e.g. [prettier-plugin-sort-imports](https://github.com/trivago/prettier-plugin-sort-imports), [eslint-plugin-import](https://github.com/import-js/eslint-plugin-import/blob/main/docs/rules/order.md) etc.

```ts
// Avoid
import { bar, foo } from '../../../../../../distant-folder';

// Use
import { locationApi } from '@api/locationApi';

import { foo } from '../../foo';
import { bar } from '../bar';
import { baz } from './baz';
```
