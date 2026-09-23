---
title: "Synchronize with auto-waiting actions and web-first assertions"
whenToRead: "Before writing, changing, reviewing, or debugging Playwright tests that wait for UI changes, such as sleeps, waitForSelector calls, visibility checks before actions, or assertions on counts or text."
impact: "MEDIUM-HIGH"
impactDescription: "Sleeps and one-shot reads make browser tests slow when the app is fast and flaky when CI is slow."
tags: "playwright, e2e, assertions, flakiness"
---

## Synchronize with auto-waiting actions and web-first assertions

Let Playwright's actions wait for elements to be ready, and assert outcomes with web-first assertions that retry until they pass.
Do not synchronize with sleeps, manual pre-waits, or values read once from the page.

### Implementation

- Perform the user's action, then assert the visible outcome, such as `await expect(locator).toBeVisible()` or `toHaveText`, `toHaveCount`, `toHaveURL`, `toBeEnabled`.
- Do not assert visibility before `click()` or `fill()`; actions already wait for the element to be visible, stable, and enabled.
  Assert visibility only when appearing is itself the behavior under test.
- Replace `expect(await locator.count()).toBe(n)` with `await expect(locator).toHaveCount(n)`, and similarly for text and attributes.
- Replace `waitForSelector` pre-waits with an assertion that states the expected outcome.
- For state with no visible signal, such as a persisted side effect, use `expect.poll(...)` or `expect(async () => { ... }).toPass()`.
- Do not use `page.waitForTimeout` to synchronize tests; it is acceptable for local debugging or to pace a recorded demo after asserting the state.
- Prefer asserting what users see, and assert internals such as request counts only when that wiring is what the test guards.

### Rationale

A fixed sleep is either longer than needed, which slows every run, or shorter than CI sometimes needs, which makes the test flaky.
A value read once from the page races the render.
Web-first assertions retry until the expected state appears or the timeout expires, then fail with the actual state, which makes failures both rarer and easier to read.

### Examples

**Incorrect (counterexample):**

```ts
test('should archive a record', async ({ page }) => {
  await page.goto('/');
  const archiveButton = page.getByRole('button', { name: 'Archive' });
  await expect(archiveButton).toBeVisible();
  await archiveButton.click();
  await page.waitForTimeout(2000);
  expect(await page.getByText('Archived').count()).toBe(1);
});
```

The visibility check is redundant, the sleep is arbitrary, and the count is read once whether or not the page has updated.

**Correct:**

```ts
test('should archive a record', async ({ page }) => {
  await page.goto('/');
  await page.getByRole('button', { name: 'Archive' }).click();
  await expect(page.getByText('Archived')).toBeVisible();
});
```

### Validation

Search tests for `waitForTimeout`, `waitForSelector`, and `expect(await ...)` patterns, and replace each with a retrying assertion.
Run the suite with CPU throttling or repeated runs, such as `--repeat-each`, and check that it passes consistently.

A `waitForTimeout` in a recorded demo, after asserting the state being shown, is not a violation.
