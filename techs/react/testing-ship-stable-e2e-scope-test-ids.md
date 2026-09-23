---
title: "Ship Stable E2E Scope Test Ids"
whenToRead: "Before implementing React components that serve as stable scopes for end-to-end tests."
impact: "MEDIUM"
impactDescription: "gives tests stable scope anchors for domain objects and persistent app chrome decided at authoring time"
tags: "react, testing, data-testid, testid, identity, scoping, e2e, playwright, components, app-chrome"
---

## Ship Stable E2E Scope Test Ids

End-to-end tests can scope to
a stable surface by test id, then select controls inside it by role and
accessible name. That contract only works if components provide the scope
hook. When a component renders repeated, data-derived, structurally complex,
or cross-route app-chrome UI - tree items, table rows, cards, panels,
dialogs, record-backed singleton surfaces such as a record editor, and
persistent controls such as topbar search - give the *container* a
`data-testid` at authoring time, not retroactively when a spec author
discovers there is no way to address one instance without `nth(...)`,
placeholder text, or layout assumptions.

**Incorrect:**

```tsx
// A preformatted test-id prop makes every caller a naming site, so the
// formats drift apart ("recordItem-3", "record_item_3", "item-3") -
// and an unidentified instance (no prop at all) is reachable only by
// position or by hoping its name text stays globally unique.
type Entry = { id: string; name: string };

function RecordItem({
  record,
  testId,
}: {
  record: Entry;
  testId: string;
}) {
  return <li data-testid={testId}>{/* … */}</li>;
}

<RecordItem record={record} testId={`recordItem-${record.id}`} />;
```

**Correct:**

```tsx
// The component that represents the domain object owns its identity: it
// formats <entity>-<surface>-<stableId> from data it already receives,
// so each entity-surface pair has exactly one formatting site.
function RecordItem({ record }: { record: Entry }) {
  return <li data-testid={`record-item-${record.id}`}>{/* … */}</li>;
}

function RecordEditor({ record }: { record: Entry }) {
  return (
    <div data-testid={`record-editor-${record.id}`}>
      <textarea aria-label="Record title" value={record.name} />
    </div>
  );
}

function TopbarRecordSearch() {
  return (
    <div data-testid="topbar-record-search">
      <input aria-label="Search records" />
    </div>
  );
}
```

**Guidelines:**

- Add the test id to the **container** that represents a domain object (the
  tree item, row, card, panel, dialog, or currently loaded editor document),
  not to the buttons, links, and inputs inside it - controls are located by
  role and accessible name;
  blanket ids on controls would silence the e2e suite's accessibility signal.
- App-chrome controls that are likely to be used as cross-route e2e anchors
  should expose a stable semantic container `data-testid`, even when the inner
  control has a good accessible name. Examples: `topbar-record-search`,
  `org-switcher`, `sidebar-nav`, and `command-palette`. Put the test id on the
  owning surface/container, then locate the input or button inside by role and
  accessible name.
- Domain-identity test ids follow one grammar, all three segments
  required: **`<entity>-<surface>-<stableId>`**. Entity is the domain
  noun (`record`, `folder`, `source`); surface is the rendering kind in
  the project's vocabulary (`item` for tree items, `row` for table rows, `card`, `panel`, `dialog`); the id is
  the stable entity id verbatim - never a slug, an index, or a
  display name. Examples: `record-item-${record.id}`,
  `record-editor-${record.id}`, `folder-item-${folder.id}`,
  `source-panel-${source.id}`. Never name from implementation or styling
  (`card-wrapper`, `blue-button`, `left-pane-v2`).
- Surface is not optional even when an entity renders in only one place
  today: `entity + id` is unique in the database but not in the DOM - the
  same record can be a tree item and the open editor document at once -
  and because test ids are rename-breaking contracts, omitting surface
  now forces a breaking rename the day a second surface ships.
- The exception is a non-domain element hook such as a drag handle or canvas region. Those have no entity
  id; give them a short semantic kebab-case name (`drag-handle`) and rely
  on the enclosing domain container for uniqueness -
  `item.getByTestId("drag-handle")`, never a global query.
- The component that represents the domain object formats its own test id
  from the id it already receives. Never accept a preformatted `testId`
  string prop - if a parent must supply identity, pass the stable
  entity id and format at the render site, keeping exactly one
  formatting site per entity-surface pair.
- Singleton surfaces with a clear landmark (a page with one `h1`, a labeled
  `nav`) usually don't need a test id unless they are persistent app chrome or
  a cross-route test anchor that specs need to locate independent of page
  content.
- Shared primitives must let ids attach without plumbing: spread rest props
  onto the semantic root element where the primitive supports them, so a
  call site can pass `data-testid` to any primitive when its instance needs
  identity.
- A test id is a public contract for tests: renaming or removing one is a
  breaking change for specs, so treat it with the same care as an exported
  symbol.
- PR review prompt: for any new app chrome, search, picker, command palette,
  dialog, editor, or cross-route control, ask "How should Playwright locate
  this without `nth()`, placeholder text, or layout assumptions?"
