---
title: "Use as const satisfies for Typed Constants"
whenToRead: "Before defining a constant that must satisfy a broad TypeScript type while retaining literal values."
impact: "MEDIUM"
impactDescription: "validates constants against broad contracts while preserving literal readonly inference"
tags: "typescript, satisfies, as-const, constants, literal-types"

attribution:
  - url: "https://github.com/mkosir/typescript-style-guide/blob/86bebd58a987e23277dba02028c0ee2d6ffb5073/website/src/pages/index.mdx"
    description: "Underlying TypeScript Style Guide material; required notice is retained in NOTICE.md."
---

## Use as const satisfies for Typed Constants

The `as const satisfies` syntax is a powerful TypeScript feature that combines strict type-checking and immutability for constants. It is particularly useful when defining constants that need to conform to a specific type.

Key benefits:

- Immutability with `as const`
  - Ensures the constant is treated as readonly.
  - Narrows the types of values to their literals, preventing accidental modifications.
- Validation with `satisfies`
  - Ensures the object conforms to a broader type without widening its inferred type.
  - Helps catch type mismatches at compile time while preserving narrowed inferred types.

Array constants:

```ts
type UserRole = 'admin' | 'editor' | 'moderator' | 'viewer' | 'guest';

// Avoid constant of wide type
const DASHBOARD_ACCESS_ROLES: ReadonlyArray<UserRole> = ['admin', 'editor', 'moderator'];

// Avoid constant with incorrect values
const DASHBOARD_ACCESS_ROLES = ['admin', 'contributor', 'analyst'] as const;

// Use immutable constant of narrowed type
const DASHBOARD_ACCESS_ROLES = ['admin', 'editor', 'moderator'] as const satisfies ReadonlyArray<UserRole>;
```

Object constants:

```ts
type OrderStatus = {
  pending: 'pending' | 'idle';
  fulfilled: boolean;
  error: string;
};

// Avoid mutable constant of wide type
const IDLE_ORDER: OrderStatus = {
  pending: 'idle',
  fulfilled: true,
  error: 'Shipping Error',
};

// Avoid constant with incorrect values
const IDLE_ORDER = {
  pending: 'done',
  fulfilled: 'partially',
  error: 116,
} as const;

// Use immutable constant of narrowed type
const IDLE_ORDER = {
  pending: 'idle',
  fulfilled: true,
  error: 'Shipping Error',
} as const satisfies OrderStatus;
```
