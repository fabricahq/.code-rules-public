---
title: "Follow the Rules of Hooks"
whenToRead: "Before writing or reviewing React components or custom Hooks that call Hooks."
impact: "CRITICAL"
impactDescription: "keeps Hook state associated with a stable call order across renders"
tags: "react, hooks, rules-of-hooks, lint, purity"

attribution:
  - url: https://react.dev/reference/rules/rules-of-hooks
    description: "Official React documentation paraphrased in the source rule."
---

## Follow the Rules of Hooks

Call stateful React Hooks in a consistent order at the top level of a function component or custom Hook, before any early return. Calling them in a loop, branch, nested function, event handler, class, or `try` / `catch` can break state association across renders. React 19's `use` API is an exception: it can read a resource conditionally or in a loop, but it must still be called while rendering a component or Hook and cannot be wrapped in `try` / `catch`.

**Incorrect:**

```tsx
function Profile({ enabled }: { enabled: boolean }) {
  if (enabled) {
    const [name, setName] = useState("");
  }

  return null;
}
```

**Correct:**

```tsx
function Profile({ enabled }: { enabled: boolean }) {
  const [name, setName] = useState("");

  if (!enabled) {
    return null;
  }

  return <input value={name} onChange={(event) => setName(event.target.value)} />;
}
```

Prefer the React hooks lint rules over local judgment when changing Hook-heavy code. If the lint rule reports a dependency or call-order problem, change the structure instead of suppressing it unless there is a documented reason.

References: [React Rules of Hooks](https://react.dev/reference/rules/rules-of-hooks), [use API](https://react.dev/reference/react/use), [eslint-plugin-react-hooks](https://react.dev/reference/eslint-plugin-react-hooks).

Source: [React docs - Rules of Hooks](https://react.dev/reference/rules/rules-of-hooks). Paraphrased from official React documentation.
