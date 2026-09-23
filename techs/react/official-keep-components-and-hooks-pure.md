---
title: "Keep components and Hooks pure"
whenToRead: "Before planning, writing, changing, or reviewing the render logic of React components or Hooks, especially code that updates variables, props, state, or browser APIs while rendering."
impact: "HIGH"
impactDescription: "Side effects during render run an unpredictable number of times, which corrupts shared data and breaks concurrent rendering and Strict Mode."
tags: "react, purity, rendering"
attribution:
  - url: https://react.dev/learn/keeping-components-pure
    description: "Official React documentation paraphrased in the source rule; restructured to the rule template with a rationale, a prop-mutation example, and validation."
---

## Keep components and Hooks pure

Make component and Hook render logic pure: given the same props, state, and context, return the same result without observable side effects.
Put side effects in event handlers, Effects, or framework data-loading APIs.

### Implementation

- Do not mutate props, state, context values, module-level variables, or objects shared with other components during render.
- Do not call browser APIs with effects, such as writing to storage, changing `document`, or starting network requests, during render.
- Do not read values that change between calls, such as `Date.now()` or `Math.random()`, during render when the result is shown; read them in an event handler or Effect, or pass them in.
- Mutating values created during the same render, such as a local array built before being returned, is fine.

### Rationale

React may render a component more than once before committing, render it again in Strict Mode during development, or discard a render in concurrent rendering.
Side effects in render therefore run an unpredictable number of times.
Pure render logic makes each render safe to repeat, skip, or interrupt.

### Examples

#### Application: Collecting data during render

**Incorrect (counterexample):**

```tsx
const selectedIds: Array<string> = [];

function Row({ id, selected }: { id: string; selected: boolean }) {
  if (selected) {
    selectedIds.push(id);
  }

  return <li>{id}</li>;
}
```

Every render appends again, so the module-level list grows with duplicates and depends on render order.

**Correct:**

```tsx
function SelectedRows({ rows }: { rows: ReadonlyArray<RowData> }) {
  const selectedIds = rows.filter((row) => row.selected).map((row) => row.id);

  return selectedIds.map((id) => <li key={id}>{id}</li>);
}
```

The component derives the list from its props during render without mutating shared data.

#### Application: Transforming props

**Incorrect (counterexample):**

```tsx
function SortedList({ items }: { items: Array<Item> }) {
  items.sort((a, b) => a.name.localeCompare(b.name));
  return <List items={items} />;
}
```

`sort` reorders the parent's array in place during render.

**Correct:**

```tsx
function SortedList({ items }: { items: ReadonlyArray<Item> }) {
  const sorted = [...items].sort((a, b) => a.name.localeCompare(b.name));
  return <List items={sorted} />;
}
```

### Validation

Run the app in Strict Mode during development and check that double-invoked renders produce no duplicate effects or changed data.
Review render code for writes to anything it did not create during that render.

Mutating a local value created in the same render is not a violation.
