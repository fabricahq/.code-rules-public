---
title: "React 19 API Changes"
whenToRead: "Before changing ref forwarding or context access in a React 19 or newer component."
impact: "MEDIUM"
impactDescription: "Using the React 19 ref prop can avoid unnecessary wrappers; conditional context reads require use()."
tags: "react, composition, react19, refs, context, hooks"

attribution:
  - url: https://github.com/vercel-labs/agent-skills/blob/4ec6f84b61cd3c931046c3e6e398f3ae7de372f7/skills/composition-patterns/rules/react19-no-forwardref.md
    description: "Underlying Vercel Agent Skills rule adapted in the source corpus."
---

## React 19 API Changes

> **Warning: React 19+ only.** Skip this if you're on React 18 or earlier.

In React 19, function components can accept `ref` as a regular prop without a `forwardRef` wrapper. React also provides `use(context)` for reading context during render, including conditional reads. `useContext` remains valid for unconditional context reads.

**Legacy pattern (still supported in React 19):**

```tsx
const ComposerInput = forwardRef<TextInput, Props>((props, ref) => {
  return <TextInput ref={ref} {...props} />
})
```

**Simpler React 19 form (ref as a regular prop):**

```tsx
function ComposerInput({ ref, ...props }: Props & { ref?: React.Ref<TextInput> }) {
  return <TextInput ref={ref} {...props} />
}
```

**Valid for an unconditional read:**

```tsx
const value = useContext(MyContext)
```

**Use `use` when the context read must be conditional:**

```tsx
if (needsValue) {
  const value = use(MyContext)
  // Render with value here.
}
```

`use()` can be called conditionally or in a loop, unlike `useContext()`, but cannot be called inside `try` / `catch`. Reading context with `use()` is not supported in Server Components.

Source: [Vercel Agent Skills - composition-patterns/react19-no-forwardref.md](https://github.com/vercel-labs/agent-skills/blob/4ec6f84b61cd3c931046c3e6e398f3ae7de372f7/skills/composition-patterns/rules/react19-no-forwardref.md). Adapted with attribution.
