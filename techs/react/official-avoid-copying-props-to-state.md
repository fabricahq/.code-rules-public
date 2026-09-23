---
title: "Avoid Copying Props to State"
whenToRead: "Before initializing React state from props or synchronizing state when props change."
impact: "HIGH"
impactDescription: "prevents local state from drifting when props change"
tags: "react, props, state, derived-state, initial-state"

attribution:
  - url: https://react.dev/learn/sharing-state-between-components
    description: "Official React documentation paraphrased in the source rule."
  - url: https://github.com/mkosir/typescript-style-guide/blob/86bebd58a987e23277dba02028c0ee2d6ffb5073/website/src/pages/index.mdx
    description: "TypeScript Style Guide props-to-state guidance cited in the source rule; see the library notice for its MIT attribution."
---

## Avoid Copying Props to State

Do not copy a prop into state just to mirror it. Mirrored state goes stale when the parent passes a new prop, and synchronization effects usually add another render while still missing edge cases.

**Incorrect:**

```tsx
type EditorProps = {
  title: string;
};

function Editor({ title }: EditorProps) {
  const [draftTitle, setDraftTitle] = useState(title);

  return <input value={draftTitle} onChange={(event) => setDraftTitle(event.target.value)} />;
}
```

**Correct (controlled by the parent):**

```tsx
type EditorProps = {
  title: string;
  onTitleChange: (title: string) => void;
};

function Editor({ title, onTitleChange }: EditorProps) {
  return <input value={title} onChange={(event) => onTitleChange(event.target.value)} />;
}
```

If a prop is intentionally used only as the initial value, name it with an `initial` prefix, such as `initialTitle`, so callers do not expect later prop changes to update the local state.

References: [You Might Not Need an Effect](https://react.dev/learn/you-might-not-need-an-effect), [Sharing State Between Components](https://react.dev/learn/sharing-state-between-components), [TypeScript Style Guide - Props To State](https://mkosir.github.io/typescript-style-guide/#props-to-state).

Source: [React docs - Sharing State Between Components](https://react.dev/learn/sharing-state-between-components) and [TypeScript Style Guide - Props To State](https://mkosir.github.io/typescript-style-guide/#props-to-state). Adapted with attribution.
