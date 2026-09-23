---
title: "Prefer Unions Over Boolean Flags"
whenToRead: "Before modeling a TypeScript state with several booleans or adding another state flag."
impact: "MEDIUM"
impactDescription: "makes mutually exclusive states explicit instead of spreading state across flags"
tags: "typescript, unions, booleans, flags, state-modeling"

attribution:
  - url: "https://github.com/mkosir/typescript-style-guide/blob/86bebd58a987e23277dba02028c0ee2d6ffb5073/website/src/pages/index.mdx"
    description: "Underlying TypeScript Style Guide material; required notice is retained in NOTICE.md."
---

## Prefer Unions Over Boolean Flags

Embrace type unions, especially when type union options are mutually exclusive, instead multiple boolean flag variables.

Boolean flags have a tendency to accumulate over time, leading to confusing and error-prone code, since they hide the actual app state.

```ts
// Avoid introducing multiple boolean flag variables
const isPending, isProcessing, isConfirmed, isExpired;

// Use type union variable
type UserStatus = 'pending' | 'processing' | 'confirmed' | 'expired';
const userStatus: UserStatus;
```

When boolean flags are used and the number of possible states grows quickly, it often results in unhandled or ambiguous states. Instead, take advantage of [discriminated unions](#discriminated-union) to better manage and represent your application's state.
