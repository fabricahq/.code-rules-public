---
title: "Use Domain Scope and User-Facing Locators"
whenToRead: "Before choosing Playwright locators for repeated records, forms, app navigation, or interactive controls."
impact: "MEDIUM"
impactDescription: "prevents selector churn while keeping e2e tests aligned with accessibility and user-visible behavior"
tags: "playwright, testing, e2e, selectors, getByRole, getByLabel, data-testid, scoping, accessibility"
---

## Use Domain Scope and User-Facing Locators

Locate elements through stable product contracts, never CSS classes, DOM
structure, or layout position. Two contracts cover nearly every locator,
and most specs use them together:

1. `data-testid` answers **"which stable surface am I inside?"** - scope to
   the repeated/data-derived domain container or persistent app-chrome surface
   first.
2. Role and accessible name answer **"what control would a user choose?"**
   - select the interactive element inside that scope.

Domain scoping by test id is first-class, not a fallback: a spec touching
repeated or data-bearing UI should establish its scope up front rather than
hope some text stays globally unique. What stays user-facing is the
*control* selection - that is what keeps every journey doubling as an
accessibility audit. Use retrying assertions for synchronization after choosing a locator.

"Data-bearing" includes singleton surfaces when the surface is still a
particular domain object: an open record editor, an account settings form, a
record detail panel, or any route body whose controls mutate one loaded
record. If the assertion means "inside this record or account," scope to
that domain container by `data-testid` first, even if there is only one title
field on screen today. Skip the domain scope only for truly global shell
landmarks or anonymous pages whose identity is already expressed by a unique
role, heading, or route.

Persistent app chrome is the parallel non-domain case: global search, command
palettes, account switchers, and sidebar navigation are cross-route test anchors.
Scope to the chrome surface by semantic test id, then select the actual
control by role and accessible name so the spec stays stable without losing
its accessibility signal.

**Incorrect:**

```ts
test("should open a record from the tree", async ({ page }) => {
  await page.goto("/");

  // Layout-coupled: breaks on any markup, styling, or ordering change,
  // and says nothing about which record the user chose.
  await page.locator("div.tree > div.row:nth-child(3) a").click();
});
```

**Correct:**

```ts
test("should open a record from the tree", async ({ page }) => {
  await page.goto("/");

  // Test id identifies the record's tree item; role + name picks the
  // control a user would choose inside it.
  const item = page.getByTestId(`record-item-${record.id}`);
  await item.getByRole("link", { name: record.name }).click();
});
```

```ts
test("should show the loaded record title", async ({ page }) => {
  await page.goto(`/records/${record.id}`);

  // The editor is the loaded record's domain surface; the title field
  // inside it is still selected by role and accessible name.
  const editor = page.getByTestId(`record-editor-${record.id}`);
  await expect(
    editor.getByRole("textbox", { name: "Record title" }),
  ).toHaveValue(record.name);
});
```

```ts
test("should search records from app chrome", async ({ page }) => {
  await page.goto("/records");

  const search = page.getByTestId("topbar-record-search");
  await search
    .getByRole("combobox", { name: "Search records" })
    .fill("Core Values");
});
```

**Guidelines:**

- Treat `data-testid` as a planned, test-facing identity hook, not merely a
  last resort. When a component renders repeated, data-derived, or
  structurally complex UI - tree items, table rows, cards, panels, dialogs,
  and record-backed singleton surfaces such as a record editor - ship it
  with a test id at authoring time so specs can scope to one instance.
- For persistent app chrome, scope to the chrome surface by semantic test id,
  then use role/name inside it:
  `page.getByTestId("topbar-record-search").getByRole("combobox", { name: "Search records" })`.
  This keeps tests stable across routes without bypassing accessibility checks.
- Reach for a test id whenever the alternative is brittle: `nth(...)`, long
  `filter({ hasText })` chains, layout-coupled selectors, or text that is
  not the identity being tested.
- Use test ids to scope, not to bypass accessible names. Buttons, links,
  inputs, headings, and tabs are still selected by role and name inside the
  scoped container - a test id on every control would silence the suite's
  accessibility signal.
- Within a scope (or for singleton UI), follow the official Playwright
  locator priority: `getByRole` with accessible name for interactive
  elements ("the closest way to how users and assistive technology
  perceive the page"), `getByLabel` for form fields (`getByPlaceholder` is
  a weaker contract - prefer a real label), `getByText` for stable
  non-interactive content that is itself the behavior under test, and
  `getByAltText` for meaningful images.
- A test id is also the honest locator for individual elements with no
  useful role or accessible name (drag handles, canvas regions, purely
  visual affordances), for visible copy genuinely expected to churn while
  the journey stays the same, and, in a localized product, for names
  whose translation would break the test.
- Domain test ids can follow a stable `<entity>-<surface>-<id>` grammar in the project's own vocabulary, such as `record-item-${id}`. Avoid styling or implementation names like `card-wrapper`. App-chrome test ids can use short semantic names such as `topbar-record-search`.
- A failure caused by a renamed control is usually signal, not noise: the
  user experience changed, and the one-line fix doubles as a review of that
  change. The inverse - a test id that keeps passing while a refactor
  silently drops an element's accessible name - is how accessibility
  regressions ship.
- Do not stabilize a test by adding an `aria-label` that diverges from
  visible text. Voice-control users speak the visible label (WCAG "Label in
  Name"), so a hidden test-only name is an accessibility bug. When visible
  text cannot be the contract, use a test id honestly.
- Pass `exact: true` when one accessible name can embed another - rows
  aggregate their children's labels, and "Name" is a substring of
  "Rename". A strict-mode violation listing several candidates is the
  usual symptom.
