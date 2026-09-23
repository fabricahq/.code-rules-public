---
title: "Use Auto-Waiting Actions and Web-First Assertions"
whenToRead: "Before writing or reviewing Playwright waits, actions, or assertions for asynchronous UI behavior."
impact: "MEDIUM"
impactDescription: "prevents flaky e2e synchronization caused by sleeps, one-shot reads, and redundant pre-waits"
tags: "playwright, testing, e2e, waits, assertions, flakiness, auto-wait, waitForTimeout"
---

## Use Auto-Waiting Actions and Web-First Assertions

Playwright already has two synchronization tools: **actions auto-wait for
actionability** (`click` and `fill` wait for visible, stable, and enabled),
and **web-first assertions retry until the expected outcome holds**
(`toBeVisible`, `toHaveText`, `toHaveCount`, `toBeEnabled`, `toBeChecked`,
`toHaveURL`). Use those instead of sleeps, manual pre-waits, or one-shot
DOM reads. The core pattern of every spec step:

1. Perform the user action.
2. Assert the user-visible outcome.
3. Let Playwright retry until the timeout.

Choose locators by accessible role and name, scoped to a stable surface when needed.

**Incorrect:**

```ts
test("should archive a record", async ({ page }) => {
  await page.goto("/");

  const archiveButton = page.getByRole("button", { name: "Archive" });
  // Redundant pre-wait: click() already waits for actionability.
  await expect(archiveButton).toBeVisible();
  await archiveButton.click();

  // Hard sleep: too slow when the page is fast, flaky when CI is slow.
  await page.waitForTimeout(2000);

  // One-shot read: samples the DOM once instead of retrying the outcome.
  expect(await page.getByText("Archived").count()).toBe(1);
});
```

**Correct:**

```ts
test("should archive a record", async ({ page }) => {
  await page.goto("/");

  await page.getByRole("button", { name: "Archive" }).click();

  // Retries until the outcome holds, then fails with context.
  await expect(page.getByText("Archived")).toBeVisible();
});
```

**Guidelines:**

- Do not pre-wait before actions: `click()` and `fill()` already wait for
  the element to be actionable. Assert visibility only when the appearance
  itself is the behavior under test (a landmark rendering, an empty state
  showing).
- Do not use `page.waitForTimeout(...)` to synchronize regression tests. It remains useful for local debugging or deliberate video pacing after asserting the state to show.
- Prefer retrying assertions over one-shot reads:
  `await expect(locator).toHaveCount(1)`, never
  `expect(await locator.count()).toBe(1)` - the former retries until the
  outcome holds, the latter races the render.
- Do not use `waitForSelector` as a pre-wait when a locator assertion
  describes the real outcome - `await expect(locator).toBeVisible()` says
  what the spec means and retries the same way.
- Assert user-visible outcomes: URL, visible text, enabled or checked
  state, row presence, empty states, navigation. Assert internals like
  network request counts only when the spec specifically exists to guard
  that wiring.
- For async state with no DOM signal (a store flag, a persisted side
  effect), the rare sanctioned waits are `expect.poll(...)` and
  `expect(async () => { ... }).toPass()` - not sleeps.
