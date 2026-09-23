---
title: "Give repeated and persistent surfaces stable test ids"
whenToRead: "Before planning, writing, changing, or reviewing React components that render repeated or data-backed surfaces, such as list items, table rows, cards, panels, dialogs, editors, or persistent app chrome that end-to-end tests need to locate."
impact: "MEDIUM"
impactDescription: "Without a stable scope, end-to-end tests fall back to positions, placeholder text, or layout assumptions and break when the UI changes."
tags: "react, testing, e2e, test-ids"
---

## Give repeated and persistent surfaces stable test ids

Give the container element of each repeated, data-backed, or persistent surface a stable `data-testid` when you author the component.
Tests scope to that container by test id, then find controls inside it by role and accessible name.

### Implementation

- Put the test id on the container that represents the domain object, such as the list item, row, card, panel, dialog, or loaded editor.
  Do not put test ids on the buttons, links, and inputs inside it; tests locate those by role and name.
- Format domain test ids as `<entity>-<surface>-<stableId>`, such as `record-item-${record.id}` or `record-editor-${record.id}`.
  Use the domain noun for the entity, the rendering kind for the surface, and the entity's stable id verbatim, never an index, slug, or display name.
- Include the surface even when the entity renders in only one place today.
  The same record can appear as a list item and an open editor at once, and adding the surface later is a breaking rename.
- Let the component that represents the object format its own test id from the id it already receives.
  Do not accept a preformatted `testId` string prop, which lets each caller invent a different format.
- Give persistent app chrome that tests use across routes a semantic test id on its container, such as `topbar-record-search`.
- Give non-domain hooks inside a scoped container, such as a drag handle, a short kebab-case name, and query them within the container.
- Let shared primitives pass `data-testid` through to their root element.
- Treat test ids as a public contract: renaming one breaks tests.

This naming grammar is a convention; a project may choose a different one, as long as it has exactly one format and one formatting site per entity and surface.

### Rationale

End-to-end tests need a way to address one instance of a repeated surface.
Without a stable scope, test authors fall back to `nth()`, placeholder text, or layout, all of which change for unrelated reasons.
Adding the scope when the component is written is cheaper than retrofitting it after a test fails, and one formatting site keeps the ids consistent.

### Examples

**Incorrect (counterexample):**

```tsx
function RecordItem({ record, testId }: { record: Entry; testId: string }) {
  return <li data-testid={testId}>{record.name}</li>;
}

<RecordItem record={record} testId={`recordItem-${record.id}`} />;
```

Each caller formats the id, so formats drift, and an instance rendered without the prop can only be found by position.

**Correct:**

```tsx
function RecordItem({ record }: { record: Entry }) {
  return <li data-testid={`record-item-${record.id}`}>{record.name}</li>;
}
```

### Validation

For each new repeated, data-backed, dialog, editor, or persistent chrome surface, ask how a test would locate one instance without `nth()`, placeholder text, or layout assumptions.
Check that the answer is a container test id in the project's format plus role-and-name queries inside it.

A singleton surface with a clear landmark, such as a page with one heading or a labeled `nav`, does not need a test id unless tests use it as a cross-route anchor.
