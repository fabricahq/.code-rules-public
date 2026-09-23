---
title: "Use Const Assertions for Constants"
whenToRead: "Before defining literal TypeScript constants whose exact values should remain in their inferred types."
impact: "MEDIUM"
impactDescription: "preserves literal values and readonly object or array constants"
tags: "typescript, as-const, constants, literal-types, readonly"

attribution:
  - url: "https://github.com/mkosir/typescript-style-guide/blob/86bebd58a987e23277dba02028c0ee2d6ffb5073/website/src/pages/index.mdx"
    description: "Underlying TypeScript Style Guide material; required notice is retained in NOTICE.md."
---

## Use Const Assertions for Constants

Strive declaring constants using const assertion `as const`:

Constants are used to represent values that are not meant to change, ensuring reliability and consistency in a codebase. Using const assertions further enhances type safety and immutability, making your code more robust and predictable.

- Type Narrowing - Using `as const` ensures that literal values (e.g., numbers, strings) are treated as exact values instead of generalized types like `number` or `string`.
- Immutability - Objects and arrays get readonly properties, preventing accidental mutations.

Examples:

- Objects

  ```ts
  // Avoid
  const FOO_LOCATION = { x: 50, y: 130 }; // Type { x: number; y: number; }
  FOO_LOCATION.x = 10;

  // Use
  const FOO_LOCATION = { x: 50, y: 130 } as const; // Type '{ readonly x: 50; readonly y: 130; }'
  FOO_LOCATION.x = 10; // Error
  ```

- Arrays

  ```ts
  // Avoid
  const BAR_LOCATION = [50, 130]; // Type number[]
  BAR_LOCATION.push(10);

  // Use
  const BAR_LOCATION = [50, 130] as const; // Type 'readonly [10, 20]'
  BAR_LOCATION.push(10); // Error
  ```

- Template Literals

  ```ts
  // Avoid
  const RATE_LIMIT = 25;
  const RATE_LIMIT_MESSAGE = `Max number of requests/min is ${RATE_LIMIT}.`; // Type string

  // Use
  const RATE_LIMIT = 25;
  const RATE_LIMIT_MESSAGE = `Max number of requests/min is ${RATE_LIMIT}.` as const; // Type 'Rate limit exceeded! Max number of requests/min is 25.'
  ```
