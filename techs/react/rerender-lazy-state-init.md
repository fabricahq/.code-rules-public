---
title: "Initialize expensive state lazily"
whenToRead: "Before writing, changing, or reviewing a React useState or useReducer call whose initial value is computed, such as parsing stored data or building an index."
impact: "LOW-MEDIUM"
impactDescription: "An initial value expression runs on every render even though React uses it only once."
tags: "react, state, performance"
attribution:
  - url: https://github.com/vercel-labs/agent-skills/blob/4ec6f84b61cd3c931046c3e6e398f3ae7de372f7/skills/react-best-practices/rules/rerender-lazy-state-init.md
    description: "Adapted from the Vercel Agent Skills rule rerender-lazy-state-init: restructured to the rule template with a rationale and validation."
---

## Initialize expensive state lazily

When the initial state comes from a computation, pass a function to `useState`, such as `useState(() => buildIndex(items))`, instead of the computed value.

### Implementation

- Use the function form for parsing, building data structures, and reading from storage or the DOM.
- A literal or an already available value, such as `useState(0)` or `useState(props.value)`, does not need it.
- For `useReducer`, pass an `init` function as the third argument.
- Reading browser storage in an initializer still runs during server rendering; guard it or read it on the client.

### Rationale

JavaScript evaluates a function call's arguments before the call, so `useState(buildIndex(items))` runs `buildIndex` on every render.
React uses the argument only on the first render, so every later computation is wasted.
An initializer function runs only on the first render.

### Examples

**Incorrect (counterexample):**

```tsx
const [index, setIndex] = useState(buildSearchIndex(items));
```

**Correct:**

```tsx
const [index, setIndex] = useState(() => buildSearchIndex(items));
```

### Validation

Check `useState` and `useReducer` calls whose initial value is a function call or other non-trivial expression.

A cheap literal or variable passed directly is not a violation.
