---
title: "Keep store state serializable"
whenToRead: "Before planning, writing, changing, or reviewing Zustand store fields, especially stores that hold DOM nodes, connections, timers, promises, class instances, Maps, or Sets."
impact: "MEDIUM"
impactDescription: "Live objects in store state break persistence, devtools, and tests, and leak resources whose lifetime nothing manages."
tags: "zustand, state, serialization, persistence"
---

## Keep store state serializable

Store plain data in Zustand: strings, numbers, booleans, `null`, arrays, and plain objects.
Keep DOM nodes, sockets, timers, promises, abort controllers, and other runtime resources in the code that owns their lifetime.

### Implementation

- Store IDs, statuses, and plain data instead of live objects, such as `selectedFileId` instead of an input element.
- Keep DOM nodes in refs, sockets and timers in Effects or services, and promises in the async code that awaits them.
- Represent sets and maps as arrays or plain objects keyed by ID, such as `Record<string, true>`.
- A non-persisted store may hold a runtime object when one owner clearly creates and disposes of it; document that ownership.

### Rationale

Persisted state is serialized to JSON, where DOM nodes and connections cannot go and `Map` and `Set` become empty objects.
Devtools and test snapshots also show live objects poorly.
A resource stored in shared state has no clear owner to close it, so it tends to leak.

### Examples

**Incorrect (counterexample):**

```ts
type UploadStore = {
  inputElement: HTMLInputElement | null;
  socket: WebSocket | null;
  dirtyFieldIds: Set<string>;
};
```

**Correct:**

```ts
type UploadStore = {
  selectedFileId: string | null;
  connectionStatus: 'idle' | 'connecting' | 'connected' | 'error';
  dirtyFieldIds: Record<string, true>;
};
```

The store records what the UI needs to know; the input element and socket stay with the code that manages them.

### Validation

Check each store field's type for DOM types, connections, timers, promises, class instances, `Map`, and `Set`.
For persisted stores, check that a save-and-reload round trip restores every field unchanged.

A documented, non-persisted runtime handle with a single owner is not a violation.
