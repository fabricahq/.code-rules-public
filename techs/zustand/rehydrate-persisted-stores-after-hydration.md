---
title: "Rehydrate persisted stores after React hydration"
whenToRead: "Before planning, writing, changing, or reviewing a Zustand store that uses persist or other browser-only data in an app with server rendering, or diagnosing hydration mismatches caused by stored values."
impact: "HIGH"
impactDescription: "A persisted store restored before React hydrates renders different content than the server did, which causes hydration errors."
tags: "zustand, persist, ssr, hydration"
---

## Rehydrate persisted stores after React hydration

In server-rendered apps, create persisted stores with `skipHydration: true`, and call `store.persist.rehydrate()` in an Effect after the app mounts.
Render the default state until then, so the first client render matches the server.

### Implementation

- Set `skipHydration: true` in the `persist` options of stores rendered on the server.
- Call `usePreferencesStore.persist.rehydrate()` in a `useEffect` near the app root, once per persisted store.
- Where the UI must distinguish "not yet restored" from the default, track it with `persist.hasHydrated()` and `persist.onFinishHydration`, or a flag set in `onRehydrateStorage`.
- Render deterministic fallback UI until the stored value is available.
- Do not read browser-only stores in React Server Components.
- Client-only apps without server rendering can keep the default automatic hydration.

### Rationale

By default, `persist` restores stored state when the store is created, and with synchronous storage such as `localStorage` that happens before React hydrates.
The client's first render then uses the stored value while the server rendered the default, so React reports a hydration mismatch.
A hydration flag set during that same restore is already true on the first render, so it does not help.
Skipping automatic hydration and restoring in an Effect makes the first client render match the server.

### Examples

**Incorrect (counterexample):**

```tsx
export const usePreferencesStore = create<PreferencesStore>()(
  persist(
    (set) => ({
      theme: 'system',
      hasHydrated: false,
      setTheme: (theme) => set({ theme }),
    }),
    { name: 'preferences', onRehydrateStorage: () => () => usePreferencesStore.setState({ hasHydrated: true }) },
  ),
);
```

With `localStorage`, the store is restored and `hasHydrated` becomes true before React hydrates, so the client's first render still differs from the server's.

**Correct:**

```tsx
export const usePreferencesStore = create<PreferencesStore>()(
  persist(
    (set) => ({
      theme: 'system',
      setTheme: (theme) => set({ theme }),
    }),
    { name: 'preferences', skipHydration: true },
  ),
);

function PersistedStoresRehydrator() {
  useEffect(() => {
    void usePreferencesStore.persist.rehydrate();
  }, []);
  return null;
}
```

The first client render uses `'system'` like the server, and the stored theme applies after mount.

### Validation

Load a server-rendered page with a non-default value stored, and check the console for hydration warnings.
Check that persisted stores used in server-rendered components set `skipHydration: true` and are rehydrated in an Effect.

A persisted store in a client-only app without server rendering is not a violation.
