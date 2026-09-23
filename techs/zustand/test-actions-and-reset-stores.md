---
title: "Test Actions and Reset Stores"
whenToRead: "Before writing tests for Zustand actions or components that share a module-level store."
impact: "MEDIUM"
impactDescription: "keeps store tests focused and prevents module-level state from leaking between test cases"
tags: "zustand, testing, actions, reset-state, isolation"
---

## Test Actions and Reset Stores

Test Zustand action behavior directly when possible, and reset module-level stores between tests. Component tests should cover UI integration, not every store transition.

**Incorrect:**

```tsx
test("selects a block", async () => {
  render(<Editor />);

  await user.click(screen.getByRole("button", { name: "Block 1" }));

  expect(screen.getByTestId("selected-block")).toHaveTextContent("Block 1");
});

test("starts with no selected block", () => {
  render(<Editor />);

  // This can fail if the previous test left the singleton store dirty.
  expect(screen.getByTestId("selected-block")).toHaveTextContent("None");
});
```

**Correct:**

```ts
const initialEditorState = {
  selectedBlockId: null,
  dirtyFieldIds: new Set<string>(),
};

beforeEach(() => {
  useEditorStore.setState(initialEditorState, true);
});

test("selects a block", () => {
  useEditorStore.getState().selectBlock("block-1");

  expect(useEditorStore.getState().selectedBlockId).toBe("block-1");
});

test("clears selection", () => {
  useEditorStore.setState({ selectedBlockId: "block-1" });

  useEditorStore.getState().clearSelection();

  expect(useEditorStore.getState().selectedBlockId).toBeNull();
});
```

**Guidelines:**

- Test actions directly for state-machine transitions, resets, persistence helpers, and selector behavior.
- Reset each store to its initial state in `beforeEach` when tests touch singleton stores.
- Mock server-state libraries or service boundaries directly instead of routing fetched data through Zustand for test convenience.
- Use component tests for UI behavior that depends on store subscription, rendering, accessibility, or user interaction.

References: Synthesized from the Zustand guidance sources listed in the [public library notice](https://github.com/fabricahq/.code-rules-public/blob/main/NOTICE.md).
