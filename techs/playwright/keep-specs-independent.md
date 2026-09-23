---
title: "Keep Specs Independent and Order-Free"
whenToRead: "Before writing or reviewing Playwright tests that share workers, fixtures, or persisted test data."
impact: "MEDIUM"
impactDescription: "lets the suite run fully parallel and keeps one failure from cascading into many"
tags: "playwright, testing, e2e, isolation, parallelism, independence, fixtures"
---

## Keep Specs Independent and Order-Free

Playwright tests may run in any worker, in any order, possibly alongside
neighboring tests. Design each test to run alone and under parallel execution.
Every test owns its whole arc: it navigates from its own `page.goto(...)`, creates any data it
mutates (named uniquely to that test), and never reads module-level state
another test wrote. A spec that depends on its predecessor passes alone and
flakes in the suite - the most expensive kind of failure to debug - and
reaching for `test.describe.serial` to paper over the coupling gives up the
parallelism that keeps the suite fast.

**Incorrect:**

```ts
// Module state threaded between tests: order-dependent, breaks alone,
// breaks under parallelism, breaks on retry.
let createdName: string;

test("should create a record", async ({ page }) => {
  await page.goto("/");
  createdName = await createRecord(page, "Shared Record");
});

test("should archive the record", async ({ page }) => {
  await page.goto("/");
  await archiveRecord(page, createdName);
});
```

**Correct:**

```ts
// One journey owns its whole arc, with data unique to this test.
test("should create, then archive a record", async ({ page }) => {
  await page.goto("/");
  const name = "E2E Archive Journey";
  await createRecord(page, name);
  await archiveRecord(page, name);
});
```

**Guidelines:**

- Each test performs its own `goto` and assumes nothing about prior
  navigation, selection, or data from other tests.
- When workers share a database, data a
  test creates must be uniquely named, and assertions should anchor on the
  rows the test created - never on table-wide counts the seeded dataset or
  a neighboring test could shift.
- `test.describe.serial` is a smell, not a tool: if two tests only pass in
  sequence, merge them into one journey or make each self-sufficient.
- Shared setup belongs in fixtures or helper
  functions, never in module-level mutable state.
