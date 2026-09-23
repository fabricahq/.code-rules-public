---
title: "Distinguish null From undefined"
whenToRead: "Before modeling API fields, form values, or return values where absence may differ from an explicit empty value."
impact: "LOW"
impactDescription: "uses null for explicit absence and undefined for omitted or non-existent values"
tags: "typescript, null, undefined, absence, payloads"

attribution:
  - url: "https://github.com/mkosir/typescript-style-guide/blob/86bebd58a987e23277dba02028c0ee2d6ffb5073/website/src/pages/index.mdx"
    description: "Underlying TypeScript Style Guide material; required notice is retained in NOTICE.md."
---

## Distinguish null From undefined

In TypeScript types `null` and `undefined` many times can be used interchangeably.
Strive to:

- Use `null` to explicitly state it has no value - assignment, return function type etc.
- Use `undefined` assignment when the value doesn't exist. E.g. exclude fields in form, request payload, database query ([Prisma differentiation](https://www.prisma.io/docs/concepts/components/prisma-client/null-and-undefined)) etc.
