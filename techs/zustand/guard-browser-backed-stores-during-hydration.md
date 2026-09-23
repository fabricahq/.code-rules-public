---
title: "Guard Browser-Backed Stores During Hydration"
whenToRead: "Before using persisted or browser-only Zustand state in server-rendered React UI."
impact: "HIGH"
impactDescription: "prevents server/client mismatches from persisted or browser-only store values"
tags: "zustand, hydration, persist, ssr, browser-state"
---

## Guard Browser-Backed Stores During Hydration

Persisted stores and browser-only state should not affect server-rendered output until the client has hydrated the store. Gate storage-backed values behind a hydration flag or equivalent framework boundary.

**Incorrect:**

```tsx
export const usePreferencesStore = create<PreferencesStore>()(
  persist(
    (set) => ({
      theme: "system",
      setTheme: (theme) => set({ theme }),
    }),
    { name: "preferences" },
  ),
);

function ThemeLabel() {
  const theme = usePreferencesStore((state) => state.theme);
  return <span>{theme}</span>;
}
```

**Correct:**

```tsx
type PreferencesStore = {
  theme: ThemePreference;
  hasHydrated: boolean;
  setTheme: (theme: ThemePreference) => void;
  setHasHydrated: (hasHydrated: boolean) => void;
};

export const usePreferencesStore = create<PreferencesStore>()(
  persist(
    (set) => ({
      theme: "system",
      hasHydrated: false,
      setTheme: (theme) => set({ theme }),
      setHasHydrated: (hasHydrated) => set({ hasHydrated }),
    }),
    {
      name: "preferences",
      onRehydrateStorage: () => (state) => state?.setHasHydrated(true),
    },
  ),
);

function ThemeLabel() {
  const { theme, hasHydrated } = usePreferencesStore(
    useShallow((state) => ({
      theme: state.theme,
      hasHydrated: state.hasHydrated,
    })),
  );

  return <span>{hasHydrated ? theme : "system"}</span>;
}
```

**Guidelines:**

- Keep store modules free of direct `window`, `document`, and storage reads outside middleware configuration.
- Do not read or mutate browser-only Zustand stores from React Server Components.
- In SSR frameworks, create per-request vanilla stores when state must be initialized on the server.
- Render deterministic fallback UI until storage-backed state is available.

References: Synthesized from the Zustand guidance sources listed in the [public library notice](https://github.com/fabricahq/.code-rules-public/blob/main/NOTICE.md).
