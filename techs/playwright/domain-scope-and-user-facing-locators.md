---
title: "Scope locators by test id, then select controls by role and name"
whenToRead: "Before writing, changing, or reviewing Playwright locators, especially for repeated records, forms, dialogs, editors, or app navigation."
impact: "MEDIUM"
impactDescription: "Locators tied to CSS classes, DOM structure, or position break on unrelated changes, and test ids on every control hide accessibility regressions."
tags: "playwright, locators, accessibility, test-ids"
---

## Scope locators by test id, then select controls by role and name

Locate elements through stable product contracts: scope to the surface you mean with its `data-testid`, then select the control inside it by accessible role and name.
Never locate elements by CSS classes, DOM structure, or position.

### Implementation

- Scope to a container by test id when the test acts on one instance of repeated or data-backed UI, such as a list item, row, card, dialog, or loaded record editor, or on persistent app chrome such as global search.
- Inside the scope, select interactive elements with `getByRole` and the accessible name, form fields with `getByLabel`, stable content with `getByText`, and images with `getByAltText`.
- Use a test id for the element itself only when it has no useful role or name, such as a drag handle or canvas, or when its visible text is expected to change or be translated.
- Replace `nth()`, long `filter({ hasText })` chains, and layout selectors with a scoped locator.
- Pass `exact: true` when one accessible name contains another, such as "Name" inside "Rename".
- Do not add an `aria-label` that differs from visible text to make a control easier to test; voice-control users say the visible label.
- Skip the test id scope for global landmarks, or pages whose identity is already clear from a unique heading or route.

### Rationale

Role and name locators match how users and assistive technology find controls, so every journey also checks that controls have accessible names.
A test id scope adds a stable identity for which instance a test means, which role and name alone cannot give when many rows contain the same buttons.
Structural selectors break when markup or styling changes even though nothing the user sees has changed.

### Examples

**Incorrect (counterexample):**

```ts
await page.locator('div.tree > div.row:nth-child(3) a').click();
```

The selector breaks on any markup, styling, or ordering change, and does not say which record the test means.

**Correct:**

```ts
const item = page.getByTestId(`record-item-${record.id}`);
await item.getByRole('link', { name: record.name }).click();

const search = page.getByTestId('topbar-record-search');
await search.getByRole('combobox', { name: 'Search records' }).fill('Core Values');
```

### Validation

Search tests for `locator()` calls with CSS or XPath selectors and for `nth()`, and replace them with scoped role and name locators.
Check that test ids are on containers, and that controls are found by role and name.

A test id on an element with no accessible role or name, such as a canvas, is not a violation.
