---
title: "Separate Type Imports"
whenToRead: "Before adding or reviewing TypeScript imports or exports used only by the type checker."
impact: "MEDIUM"
impactDescription: "makes runtime dependencies distinct from type-only dependencies"
tags: "typescript, imports, import-type, bundling, tree-shaking"

attribution:
  - url: "https://github.com/mkosir/typescript-style-guide/blob/86bebd58a987e23277dba02028c0ee2d6ffb5073/website/src/pages/index.mdx"
    description: "Underlying TypeScript Style Guide material; required notice is retained in NOTICE.md."
---

## Separate Type Imports

TypeScript allows specifying a `type` keyword on imports to indicate that the export exists only in the type system, not at runtime.

Type imports must always be separated:

- Tree Shaking and Dead Code Elimination: If you use `import` for types instead of `import type`, the bundler might include the imported module in the bundle unnecessarily, increasing the size. Separating imports ensures that only necessary runtime code is included.
- Minimizing Dependencies: Some modules may contain both runtime and type definitions. Mixing type imports with runtime imports might lead to accidental inclusion of unnecessary runtime code.
- Improves code clarity by making the distinction between runtime dependencies and type-only imports explicit.

**Related automated rule:** [Reference](https://typescript-eslint.io/rules/consistent-type-imports/)

```js
'@typescript-eslint/consistent-type-imports': 'error'
```

```ts
// Avoid using `import` for both runtime and type
import { MyClass } from 'some-library';

// Even if MyClass is only a type, the entire module might be included in the bundle.

// Use `import type`
import type { MyClass } from 'some-library';

// This ensures only the type is imported and no runtime code from "some-library" ends up in the bundle.
```
