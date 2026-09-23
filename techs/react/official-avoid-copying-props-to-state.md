---
title: "Avoid copying props to state"
whenToRead: "Before planning, writing, changing, or reviewing React state that is initialized from props or kept in sync when props change."
impact: "HIGH"
impactDescription: "State copied from props goes stale when the parent passes a new value, and syncing Effects add renders while still missing cases."
tags: "react, state, props"
attribution:
  - url: https://react.dev/learn/sharing-state-between-components
    description: "Official React documentation paraphrased in the source rule; restructured to the rule template with a keyed-reset example and validation."
  - url: https://github.com/mkosir/typescript-style-guide/blob/86bebd58a987e23277dba02028c0ee2d6ffb5073/website/src/pages/index.mdx
    description: "TypeScript Style Guide props-to-state guidance cited in the source rule; see the library notice for its MIT attribution."
---

## Avoid copying props to state

Do not copy a prop into state to mirror it.
Read the prop directly, lift the state to the parent, or reset local state with a `key` when the prop identifies a different item.

### Implementation

- When the parent owns the value, make the component controlled: take the value and a change callback as props.
- When the component must keep an editable draft that starts from a prop, name the prop with an `initial` or `default` prefix, such as `initialTitle`, so callers know later changes do not update the draft.
- When the draft should restart for a different item, render the component with a `key` set to that item's identifier.
- Do not add an Effect that copies a changed prop into state.

### Rationale

`useState` uses its argument only on the first render.
A mirrored prop stops updating when the parent passes a new value, and an Effect that re-copies it renders once with the stale value, then again, and can overwrite a user's in-progress edit.

### Examples

#### Application: A value the parent owns

**Incorrect (counterexample):**

```tsx
function TitleEditor({ title }: { title: string }) {
  const [draftTitle, setDraftTitle] = useState(title);

  return <input value={draftTitle} onChange={(event) => setDraftTitle(event.target.value)} />;
}
```

When the parent passes a new `title`, the input keeps showing the old one.

**Correct:**

```tsx
function TitleEditor({
  title,
  onTitleChange,
}: {
  title: string;
  onTitleChange: (title: string) => void;
}) {
  return <input value={title} onChange={(event) => onTitleChange(event.target.value)} />;
}
```

#### Application: A draft that restarts per item

**Correct:**

```tsx
function DraftEditor({ initialTitle }: { initialTitle: string }) {
  const [draftTitle, setDraftTitle] = useState(initialTitle);

  return <input value={draftTitle} onChange={(event) => setDraftTitle(event.target.value)} />;
}

<DraftEditor key={note.id} initialTitle={note.title} />;
```

The prop name says it is only an initial value, and the `key` gives each note a fresh draft.

### Validation

For each `useState` initialized from a prop, check that the prop is named as an initial value or that the component is keyed by the item it edits.
Check that no Effect copies a prop into state.

A draft initialized from an `initial`-prefixed prop is not a violation.
