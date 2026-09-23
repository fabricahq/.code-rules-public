---
title: "Keep Function Args Mostly Required"
whenToRead: "Before designing a TypeScript function with several optional parameters or distinct modes of operation."
impact: "MEDIUM"
impactDescription: "discourages overloaded catch-all functions with many ambiguous optional arguments"
tags: "typescript, functions, arguments, optional, required"

attribution:
  - url: "https://github.com/mkosir/typescript-style-guide/blob/86bebd58a987e23277dba02028c0ee2d6ffb5073/website/src/pages/index.mdx"
    description: "Underlying TypeScript Style Guide material; required notice is retained in NOTICE.md."
---

## Keep Function Args Mostly Required

**Strive to have majority of args required and use optional sparingly.**
 If the function becomes too complex, it probably should be broken into smaller pieces.
 An exaggerated example where implementing 10 functions with 5 required args each, is better then implementing one "can do it all" function that accepts 50 optional args.
