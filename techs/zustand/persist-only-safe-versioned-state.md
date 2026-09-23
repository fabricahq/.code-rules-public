---
title: "Persist only safe, versioned state"
whenToRead: "Before planning, writing, changing, or reviewing a Zustand store that uses the persist middleware, or changing the shape of a persisted store."
impact: "HIGH"
impactDescription: "Persisting whole stores exposes tokens and personal data in browser storage, and unversioned shapes break when a release changes them."
tags: "zustand, persist, security, migrations"
---

## Persist only safe, versioned state

Persist only the fields that must survive a reload, under a unique storage key, with a version and migration for shapes that may change.
Never persist secrets or credentials.

### Implementation

- Persist state only when surviving a reload is a real requirement, such as preferences or an unsaved local draft.
- Use `partialize` to choose the fields to store, rather than persisting the whole state and its actions.
- Give each store a unique `name`, so stores cannot overwrite each other's data.
- Set `version`, and provide `migrate` to convert older stored shapes whenever the version increases.
- Do not persist access tokens, refresh tokens, other secrets, or personal data; browser storage is readable by any script on the page.
- In server-rendered apps, also skip automatic hydration and rehydrate after mount.

### Rationale

Everything in `localStorage` is readable by any script running on the origin, including injected ones, so credentials stored there can be stolen.
Stored data also outlives the code that wrote it; without a version and migration, a release that changes the state shape reads old data in the wrong shape.

### Examples

**Incorrect (counterexample):**

```ts
export const useSessionStore = create<SessionStore>()(
  persist(
    (set) => ({
      accessToken: null,
      profile: null,
      setSession: (session) => set(session),
    }),
    { name: 'app-store' },
  ),
);
```

The access token lands in `localStorage`, the generic name can collide with other stores, and nothing handles a future shape change.

**Correct:**

```ts
export const usePreferencesStore = create<PreferencesStore>()(
  persist(
    (set) => ({
      theme: 'system',
      density: 'comfortable',
      setTheme: (theme) => set({ theme }),
    }),
    {
      name: 'preferences',
      version: 2,
      partialize: (state) => ({ theme: state.theme, density: state.density }),
      migrate: (persisted, version) => migratePreferences(persisted, version),
    },
  ),
);
```

### Validation

Inspect browser storage after using the app and check that it holds only the intended fields, with no tokens or personal data.
Check that each persisted store has a unique name, and a `version` and `migrate` when its shape has changed.

Persisting a single preference without `migrate`, while its shape has never changed, is not a violation.
