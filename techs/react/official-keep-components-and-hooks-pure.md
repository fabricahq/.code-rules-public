---
title: "Keep Components and Hooks Pure"
whenToRead: "When planning, implementing, or reviewing computation and side effects in React component or Hook render."
impact: "HIGH"
impactDescription: "prevents render-time side effects from producing inconsistent UI under concurrent rendering"
tags: "react, purity, render, side-effects, hooks"

attribution:
  - url: https://react.dev/learn/keeping-components-pure
    description: "Official React documentation paraphrased in the source rule."
---

## Keep Components and Hooks Pure

React components and Hooks should be pure during render: given the same props, state, and context, they should return the same JSX and avoid observable side effects. Put side effects in event handlers, Effects, or framework data layers instead of directly in render.

**Incorrect:**

```tsx
const selectedIds: Array<string> = [];

function Row({ id, selected }: { id: string; selected: boolean }) {
  if (selected) {
    selectedIds.push(id);
  }

  return <li>{id}</li>;
}
```

**Correct:**

```tsx
function Row({ id }: { id: string }) {
  return <li>{id}</li>;
}

function SelectedRows({ rows }: { rows: ReadonlyArray<RowData> }) {
  const selectedIds = rows.filter((row) => row.selected).map((row) => row.id);

  return selectedIds.map((id) => <Row key={id} id={id} />);
}
```

Local mutation of values created during the same render can be fine. Mutating module-level objects, props, state, context values, or browser state during render is not.

References: [Keeping Components Pure](https://react.dev/learn/keeping-components-pure), [Components and Hooks must be pure](https://react.dev/reference/rules/components-and-hooks-must-be-pure).

Source: [React docs - Keeping Components Pure](https://react.dev/learn/keeping-components-pure). Paraphrased from official React documentation.
