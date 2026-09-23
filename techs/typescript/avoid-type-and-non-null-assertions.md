---
title: "Avoid Type and Non-null Assertions"
whenToRead: "Before adding or reviewing TypeScript type assertions or non-null assertions."
impact: "HIGH"
impactDescription: "prevents assertions from silencing compiler errors that can become runtime crashes"
tags: "typescript, assertions, non-null, type-safety, runtime"

attribution:
  - url: "https://github.com/mkosir/typescript-style-guide/blob/86bebd58a987e23277dba02028c0ee2d6ffb5073/website/src/pages/index.mdx"
    description: "Underlying TypeScript Style Guide material; required notice is retained in NOTICE.md."
---

## Avoid Type and Non-null Assertions

Type assertions `user as User` and non-nullability assertions `user!.name` are unsafe. Both only silence TypeScript compiler and increase the risk of crashing application at runtime.
They can only be used as an exception (e.g. third party library types mismatch, dereferencing `unknown` etc.) with a strong rational for why it's introduced into the codebase.

```ts
type User = { id: string; username: string; avatar: string | null };
// Avoid type assertions
const user = { name: 'Nika' } as User;
// Avoid non-nullability assertions
renderUserAvatar(user!.avatar); // Runtime error

const renderUserAvatar = (avatar: string) => {...}
```
