---
title: "Do not wrap a simple expression with a primitive result type in useMemo"
whenToRead: "Before wrapping a cheap primitive expression in React useMemo."
impact: "LOW-MEDIUM"
impactDescription: "Memoizing a cheap expression can add overhead and obscure simple render logic."
tags: "react, performance, rerender, useMemo, optimization"

attribution:
  - url: https://github.com/vercel-labs/agent-skills/blob/4ec6f84b61cd3c931046c3e6e398f3ae7de372f7/skills/react-best-practices/rules/rerender-simple-expression-in-memo.md
    description: "Underlying Vercel Agent Skills rule adapted in the source corpus."
---

## Do not wrap a simple expression with a primitive result type in useMemo

When an expression is simple (few logical or arithmetical operators) and has a primitive result type (boolean, number, string), do not wrap it in `useMemo`.
Calling `useMemo` and comparing hook dependencies may consume more resources than the expression itself.

**Incorrect:**

```tsx
function Header({ user, notifications }: Props) {
  const isLoading = useMemo(() => {
    return user.isLoading || notifications.isLoading
  }, [user.isLoading, notifications.isLoading])

  if (isLoading) return <Skeleton />
  // return some markup
}
```

**Correct:**

```tsx
function Header({ user, notifications }: Props) {
  const isLoading = user.isLoading || notifications.isLoading

  if (isLoading) return <Skeleton />
  // return some markup
}
```

Source: [Vercel Agent Skills - react-best-practices/rerender-simple-expression-in-memo.md](https://github.com/vercel-labs/agent-skills/blob/4ec6f84b61cd3c931046c3e6e398f3ae7de372f7/skills/react-best-practices/rules/rerender-simple-expression-in-memo.md). Adapted with attribution.
