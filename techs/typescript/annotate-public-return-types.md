---
title: "Annotate Public Return Types"
whenToRead: "Before defining or reviewing exported TypeScript functions and library APIs consumed outside their module."
impact: "MEDIUM"
impactDescription: "protects exported and boundary functions from accidental return-type drift"
tags: "typescript, functions, return-types, public-api, annotations"

attribution:
  - url: "https://github.com/mkosir/typescript-style-guide/blob/86bebd58a987e23277dba02028c0ee2d6ffb5073/website/src/pages/index.mdx"
    description: "Underlying TypeScript Style Guide material; required notice is retained in NOTICE.md."
---

## Annotate Public Return Types

Requiring explicit return types improves safety, catches errors early, and helps with long-term maintainability. However, excessive strictness can slow development and add unnecessary redundancy.

As a rule of thumb, be explicit on the outside, implicit on the inside. For example, when building APIs or libraries, always type everything explicitly to avoid accidental breaking changes. For internal logic, let TypeScript infer its defaults, which will provide strong type safety without added verbosity.

Consider the advantages of explicitly defining the return type of a function:

- **Improves Readability**: Clearly specifies what type of value the function returns, making the code easier to understand for those calling the function.
- **Avoids Misuse**: Ensures that calling code does not accidentally attempt to use an undefined value when no return value is intended.
- **Surfaces Type Errors Early**: Helps catch potential type errors during development, especially when code changes unintentionally alter the return type.
- **Simplifies Refactoring**: Ensures that any variable assigned to the function's return value is of the correct type, making refactoring safer and more efficient.
- **Encourages Design Discussions**: Similar to Test-Driven Development (TDD), explicitly defining function arguments and return types promotes discussions about a function's functionality and interface ahead of implementation.
- **Optimizes Compilation**: While TypeScript's type inference is powerful, explicitly defining return types can reduce the workload on the TypeScript compiler, improving overall performance.

As context matters, use explicit return types when they add clarity and safety.

**Related automated rule:** Explicitly defining the return type of a function is encouraged, although not required [Reference](https://typescript-eslint.io/rules/explicit-function-return-type/)

```js
"@typescript-eslint/explicit-function-return-type": "error"
```
