---
title: "Follow the Rules of Hooks"
whenToRead: "Before planning, writing, changing, or reviewing React components or custom Hooks that call Hooks, or when a Hooks lint warning appears."
impact: "HIGH"
impactDescription: "Calling Hooks conditionally or out of order attaches state to the wrong Hook and produces bugs that are hard to trace."
tags: "react, hooks"
attribution:
  - url: https://react.dev/reference/rules/rules-of-hooks
    description: "Official React documentation paraphrased in the source rule; restructured to the rule template with a rationale, a loop example, and validation."
---

## Follow the Rules of Hooks

Call Hooks only at the top level of a function component or custom Hook, in the same order on every render, and before any early return.

### Implementation

- Do not call Hooks inside conditions, loops, nested functions, event handlers, class components, or `try` / `catch` blocks.
- Move a condition inside the Hook call, or into the logic that uses the Hook's result, instead of wrapping the Hook call in the condition.
- When a component needs a varying number of stateful items, render a child component per item, and let each child call its own Hooks.
- The `use` API is an exception: it can be called conditionally or in a loop, but only while rendering a component or Hook, and not inside `try` / `catch`.
- Enable the React Hooks lint rules.
  When they report a call-order or dependency problem, change the structure instead of suppressing the warning, unless a comment documents why the suppression is safe.

### Rationale

React identifies each Hook's state by the order of Hook calls during render.
If a call is skipped or repeated on one render, every later Hook reads the state that belonged to a different call.
The resulting bugs appear far from the conditional call, often only for some props.

### Examples

#### Application: A conditional Hook

**Incorrect (counterexample):**

```tsx
function Profile({ enabled }: { enabled: boolean }) {
  if (enabled) {
    const [name, setName] = useState('');
  }

  return null;
}
```

The Hook runs on some renders and not others, so React loses track of which state belongs to which call.

**Correct:**

```tsx
function Profile({ enabled }: { enabled: boolean }) {
  const [name, setName] = useState('');

  if (!enabled) {
    return null;
  }

  return <input value={name} onChange={(event) => setName(event.target.value)} />;
}
```

#### Application: A Hook per list item

**Incorrect (counterexample):**

```tsx
function Checklist({ items }: { items: ReadonlyArray<Item> }) {
  const checked = items.map(() => useState(false));
  // ...
}
```

The number of Hook calls changes whenever the list length changes.

**Correct:**

```tsx
function Checklist({ items }: { items: ReadonlyArray<Item> }) {
  return items.map((item) => <ChecklistRow key={item.id} item={item} />);
}

function ChecklistRow({ item }: { item: Item }) {
  const [checked, setChecked] = useState(false);
  // ...
}
```

Each row owns a fixed set of Hook calls.

### Validation

Run the React Hooks lint rules and check that they report no call-order violations.
Review any lint suppression for a comment that explains why it is safe.

A conditional or looped call to `use` is not a violation.
