---
title: "Persist Only Safe Versioned State"
whenToRead: "Before persisting Zustand state to browser storage or changing a persisted store schema."
impact: "HIGH"
impactDescription: "avoids storage collisions, stale persisted shapes, and sensitive data leaks"
tags: "zustand, persist, localstorage, migrations, security"
---

## Persist Only Safe Versioned State

Use `persist` only for client state that must survive reloads. Persist the smallest safe subset, give each store a unique storage key, and version any shape that may change.

**Incorrect:**

```ts
export const useSessionStore = create<SessionStore>()(
  persist(
    (set) => ({
      accessToken: null,
      refreshToken: null,
      profile: null,
      setSession: (session) => set(session),
    }),
    { name: "app-store" },
  ),
);
```

**Correct:**

```ts
export const usePreferencesStore = create<PreferencesStore>()(
  persist(
    (set) => ({
      theme: "system",
      density: "comfortable",
      setTheme: (theme) => set({ theme }),
      setDensity: (density) => set({ density }),
    }),
    {
      name: "example-preferences",
      version: 2,
      partialize: (state) => ({
        theme: state.theme,
        density: state.density,
      }),
      migrate: (persisted, version) => migratePreferences(persisted, version),
    },
  ),
);
```

**Guidelines:**

- Persist preferences, feature toggles, and local drafts only when reload survival is a real requirement.
- Do not persist secrets, access tokens, refresh tokens, raw PII, or long-lived authorization state to browser storage.
- Use unique storage names so unrelated stores cannot overwrite each other.
- Use `partialize`, `version`, and `migrate` when persisting anything beyond trivial preferences.

References: Synthesized from the Zustand guidance sources listed in the [public library notice](https://github.com/fabricahq/.code-rules-public/blob/main/NOTICE.md).
