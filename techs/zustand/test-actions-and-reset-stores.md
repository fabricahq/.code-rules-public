---
title: "Reset stores between tests and test actions directly"
whenToRead: "Before planning, writing, changing, or reviewing tests for code that uses Zustand stores, including tests that render components reading a module-level store."
impact: "MEDIUM"
impactDescription: "Module-level stores keep their state between tests, so tests pass or fail depending on which ran before them."
tags: "zustand, testing, test-isolation"
---

## Reset stores between tests and test actions directly

Reset every module-level store to its initial state before each test, including its actions.
Test store logic by calling actions through `getState()`, and use component tests for how the UI uses the store.

### Implementation

- Capture the complete initial state, actions included, right after creating the store, such as `const initialState = useEditorStore.getState()`.
- Before each test, restore it with `useEditorStore.setState(initialState, true)`.
- Do not reset with a hand-written object passed as a full replacement; replacing without the actions removes them from the store.
- Alternatively, mock `zustand` as its testing guide describes, so every store created in tests resets automatically.
- Test actions directly for state transitions, and render components when the behavior involves rendering, interaction, or accessibility.
- Mock the server-state layer or service boundaries directly, rather than routing fetched data through a store to make tests easier.

### Rationale

A store created at module scope lives as long as the test run.
State one test leaves behind changes the next test's starting point, so results depend on order.
`setState(state, true)` replaces the whole state object; a replacement without the action functions leaves the store with no actions, and the next call fails.

### Examples

**Incorrect (counterexample):**

```ts
beforeEach(() => {
  useEditorStore.setState({ selectedBlockId: null }, true);
});

test('selects a block', () => {
  useEditorStore.getState().selectBlock('block-1');
  // ...
});
```

The replacement object has no actions. TypeScript rejects this call for a typed store, and in untyped or cast code the reset removes `selectBlock`, so the test throws.

**Correct:**

```ts
const initialEditorState = useEditorStore.getState();

beforeEach(() => {
  useEditorStore.setState(initialEditorState, true);
});

test('selects a block', () => {
  useEditorStore.getState().selectBlock('block-1');
  expect(useEditorStore.getState().selectedBlockId).toBe('block-1');
});
```

### Validation

Run the test file in random order, or run each test alone, and check that results do not change.
Check that every reset restores a complete state that includes the actions.

A test file that never touches a store does not need a reset.
