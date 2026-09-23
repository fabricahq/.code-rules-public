---
title: "Prefer Type Aliases"
whenToRead: "Before defining a TypeScript shape for which a type alias and interface are both viable."
impact: "LOW"
impactDescription: "keeps type declarations consistent while reserving interfaces for declaration merging or extension boundaries"
tags: "typescript, type-alias, interface, consistency"

attribution:
  - url: "https://github.com/mkosir/typescript-style-guide/blob/86bebd58a987e23277dba02028c0ee2d6ffb5073/website/src/pages/index.mdx"
    description: "Underlying TypeScript Style Guide material; required notice is retained in NOTICE.md."
---

## Prefer Type Aliases

TypeScript provides two options for defining types: `type` and `interface`. While these options have some functional differences, they are interchangeable in most cases. To maintain consistency, choose one and use it consistently.

**Related automated rule:** Define all types using type alias [Reference](https://typescript-eslint.io/rules/consistent-type-definitions)

```js
'@typescript-eslint/consistent-type-definitions': ['error', 'type']
```

**Note:**

Consider using interfaces when developing a package that might be extended by third-party consumers in the future or
  when your team prefers working with interfaces. In these cases, you can disable linting rules if needed, such as when
  defining type unions (e.g. `type Status = 'loading' | 'error'`).

```ts
// Avoid interface definitions
interface UserRole = 'admin' | 'guest'; // Invalid - interfaces can't define type unions

interface UserInfo {
  name: string;
  role: 'admin' | 'guest';
}

// Use type definition
type UserRole = 'admin' | 'guest';

type UserInfo = {
  name: string;
  role: UserRole;
};

```

When performing declaration merging (e.g. extending third-party library types), use `interface` and disable the lint rule where necessary.

```ts
// types.ts
declare namespace NodeJS {
  // eslint-disable-next-line @typescript-eslint/consistent-type-definitions
  export interface ProcessEnv {
    NODE_ENV: 'development' | 'production';
    PORT: string;
    CUSTOM_ENV_VAR: string;
  }
}

// server.ts
app.listen(process.env.PORT, () => {...}
```
