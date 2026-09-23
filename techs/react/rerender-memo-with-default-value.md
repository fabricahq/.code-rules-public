---
title: "Extract Default Non-primitive Parameter Value from Memoized Component to Constant"
whenToRead: "Before giving a memoized React component a default array, object, or function prop."
impact: "MEDIUM"
impactDescription: "A new default object on each render defeats memoization based on identity."
tags: "react, performance, rerender, memo, optimization"

attribution:
  - url: https://github.com/vercel-labs/agent-skills/blob/4ec6f84b61cd3c931046c3e6e398f3ae7de372f7/skills/react-best-practices/rules/rerender-memo-with-default-value.md
    description: "Underlying Vercel Agent Skills rule adapted in the source corpus."
---

## Extract Default Non-primitive Parameter Value from Memoized Component to Constant

When memoized component has a default value for some non-primitive optional parameter, such as an array, function, or object, calling the component without that parameter results in broken memoization. This is because new value instances are created on every rerender, and they do not pass strict equality comparison in `memo()`.

To address this issue, extract the default value into a constant.

**Incorrect (`onClick` has different values on every rerender):**

```tsx
const UserAvatar = memo(function UserAvatar({ onClick = () => {} }: { onClick?: () => void }) {
  // ...
})

// Used without optional onClick
<UserAvatar />
```

**Correct (stable default value):**

```tsx
const NOOP = () => {};

const UserAvatar = memo(function UserAvatar({ onClick = NOOP }: { onClick?: () => void }) {
  // ...
})

// Used without optional onClick
<UserAvatar />
```

Source: [Vercel Agent Skills - react-best-practices/rerender-memo-with-default-value.md](https://github.com/vercel-labs/agent-skills/blob/4ec6f84b61cd3c931046c3e6e398f3ae7de372f7/skills/react-best-practices/rules/rerender-memo-with-default-value.md). Adapted with attribution.
