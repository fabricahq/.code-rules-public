---
title: "Give every interactive element a role and an accessible name"
whenToRead: "Before planning, writing, changing, or reviewing interactive React controls, such as icon-only buttons, custom dialogs, form fields, editable surfaces, or actions repeated in list rows."
impact: "HIGH"
impactDescription: "Controls without a programmatic role and name are unusable with screen readers and voice control, and tests cannot locate them by role."
tags: "react, accessibility, aria, testing"
---

## Give every interactive element a role and an accessible name

Make every interactive element expose a role and an accessible name that describe it the way users perceive it.

### Implementation

- Buttons and links with visible text already have a name.
  Give icon-only controls an `aria-label`; a `title` tooltip is not a reliable name.
  Give toggle buttons `aria-pressed` so their state is announced.
- Associate each form field with its label using `htmlFor` and `id`, generating the id with `useId`, or wrap the input in its `<label>`.
- Include the row's identity in the name of actions repeated on every row, such as "Delete invoice 1042", so each one is distinguishable.
  This matters even when the buttons are only visually hidden until hover, because they are all in the accessibility tree.
- Give custom overlays `role="dialog"`, `aria-modal="true"`, and `aria-labelledby` pointing at the visible title.
  Prefer an established dialog primitive, which also manages focus.
- Give custom editable surfaces, such as a `contenteditable` editor, `role="textbox"`, `aria-multiline` when applicable, and an accessible name.
- When a landmark such as `nav` appears more than once, distinguish each with an `aria-label`.
- When an element has visible text, make any `aria-label` include that text, so voice-control users can say what they see.
  Do not add a different name only to make an element easier to test.

### Rationale

Screen readers announce, and voice control targets, controls by their role and accessible name.
Native elements with visible text get both automatically, but icon-only buttons, custom overlays, and repeated row actions do not.
Tests that locate elements by role and name, as users do, also fail when these semantics are missing, so the gap tends to surface late.

### Examples

#### Application: An icon-only button

**Incorrect (counterexample):**

```tsx
<button onClick={onOpenMenu}>
  <MoreHorizontalIcon />
</button>
```

A screen reader announces only "button".

**Correct:**

```tsx
<button onClick={onOpenMenu} aria-label="Record actions" title="Record actions">
  <MoreHorizontalIcon />
</button>
```

#### Application: A custom dialog

**Incorrect (counterexample):**

```tsx
<div className="modal-backdrop">
  <div className="modal">
    <h2>{title}</h2>
    {children}
  </div>
</div>
```

Assistive technology does not know a dialog opened or what it is called.

**Correct:**

```tsx
function Modal({ title, children }: { title: string; children: ReactNode }) {
  const titleId = useId();

  return (
    <div className="modal-backdrop">
      <div className="modal" role="dialog" aria-modal="true" aria-labelledby={titleId}>
        <h2 id={titleId}>{title}</h2>
        {children}
      </div>
    </div>
  );
}
```

### Validation

Inspect new interactive elements in the browser's accessibility tree, or query them in tests by role and accessible name.
Each control should have the expected role and a unique, meaningful name.
An automated checker such as axe can catch missing names but not misleading ones.

A button or link whose visible text is its name needs no ARIA attributes.
