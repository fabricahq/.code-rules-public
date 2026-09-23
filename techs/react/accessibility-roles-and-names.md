---
title: "Give Every Interactive Element a Role and an Accessible Name"
whenToRead: "Before designing, implementing, or reviewing interactive React controls and their accessible roles or names."
impact: "HIGH"
impactDescription: "keeps components usable by assistive tech and locatable by user-facing test selectors"
tags: "react, accessibility, aria, aria-label, dialogs, forms, icon-buttons, contenteditable, testing"
---

## Give Every Interactive Element a Role and an Accessible Name

Role and accessible-name locators reflect how users perceive controls. Screen readers and voice control depend on the same semantics. A control without a
programmatic name is invisible to all three, and the gap surfaces late:
an element a test can't select, or an accessibility regression nothing
catches. Native elements with visible text get this for free; this rule
covers the cases that don't. The examples below cover common gaps in interactive controls.

**Incorrect:**

```tsx
// Icon-only button: no accessible name (title alone is a weak fallback).
<button onClick={onOpenMenu}>
  <MoreHorizontal className="h-4 w-4" />
</button>

// Hand-rolled modal: no dialog role, no accessible title.
<div className="fixed inset-0 z-[100] flex items-center justify-center">
  <div className="relative max-w-[400px] rounded-xl">
    <h3>{title}</h3>
    {children}
  </div>
</div>
```

**Correct:**

```tsx
<button
  onClick={onOpenMenu}
  aria-label="Record actions"
  title="Record actions"
>
  <MoreHorizontal className="h-4 w-4" />
</button>

// The dialog role plus aria-labelledby make the overlay announce and
// select as a dialog named by its visible heading.
const titleId = useId();
<div className="fixed inset-0 z-[100] flex items-center justify-center">
  <div role="dialog" aria-modal="true" aria-labelledby={titleId}>
    <h3 id={titleId}>{title}</h3>
    {children}
  </div>
</div>
```

**Guidelines:**

- Buttons and links with visible text need nothing extra. Icon-only
  controls need `aria-label` (keep `title` for the hover tooltip, but
  don't rely on it as the name). Toggle buttons also declare
  `aria-pressed` so state is announced and assertable.
- Form fields associate label and input via `htmlFor`/`id` (generate the
  id with `useId`). Use labeled form primitives when available; a native `<label>` wrapping its input also works.
- Actions repeated on every row of a list need the row woven into the
  accessible name ("Add record in Business"), especially when they are
  only *visually* hidden until hover - every row's buttons exist in the
  DOM, so identical names are ambiguous to assistive tech and tests
  alike.
- Hand-rolled overlays need `role="dialog"`, `aria-modal="true"`, and
  `aria-labelledby` pointing at the visible title. Radix primitives ship
  these semantics - prefer them for new overlay surfaces.
- Custom editable surfaces (contenteditable, TipTap) declare
  `role="textbox"`, `aria-multiline`, and an `aria-label` so they behave
  like the input they are.
- When a landmark appears more than once (multiple `nav`s), distinguish
  them with `aria-label` ("Primary").
- When an element has visible text, any `aria-label` must include that
  text (WCAG "Label in Name") - voice-control users speak what they see.
  Never add a divergent name to stabilize a test; use a stable test
  scope when necessary instead.
