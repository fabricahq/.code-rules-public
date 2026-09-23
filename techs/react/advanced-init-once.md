---
title: "Run app-wide initialization once per app load"
whenToRead: "Before planning, writing, changing, or reviewing React code that performs app-wide setup, such as reading persisted settings, checking an auth token, or initializing an SDK."
impact: "LOW-MEDIUM"
impactDescription: "Initialization placed in a component Effect runs again on remount and twice in development, repeating setup that must happen once."
tags: "react, effects, initialization"
attribution:
  - url: https://github.com/vercel-labs/agent-skills/blob/4ec6f84b61cd3c931046c3e6e398f3ae7de372f7/skills/react-best-practices/rules/advanced-init-once.md
    description: "Adapted from the Vercel Agent Skills rule advanced-init-once: restructured to the rule template with a rationale and validation."
---

## Run app-wide initialization once per app load

Run setup that must happen once per app load in the entry module or behind a module-level guard, not in a component's mount Effect.

### Implementation

- Prefer calling app-wide setup in the application's entry module, before rendering, when it does not need React.
- When it must start from a component, guard it with a module-level flag so a remount does not repeat it.
- Guard only browser-side setup this way; on a server, module state is shared across requests.
- Setup that belongs to a component instance, such as subscribing while a widget is displayed, belongs in an Effect with cleanup instead.

### Rationale

Components can unmount and mount again, and Strict Mode runs mount Effects twice in development to surface missing cleanup.
Setup that must happen once per load, such as initializing an analytics SDK, then runs more than once.

### Examples

**Incorrect (counterexample):**

```tsx
function App() {
  useEffect(() => {
    loadSettingsFromStorage();
    checkAuthToken();
  }, []);
  // ...
}
```

The setup runs twice in development and again whenever `App` remounts.

**Correct:**

```tsx
let didInit = false;

function App() {
  useEffect(() => {
    if (didInit) return;
    didInit = true;
    loadSettingsFromStorage();
    checkAuthToken();
  }, []);
  // ...
}
```

### Validation

Run the app in Strict Mode during development and check that app-wide setup runs once.

An Effect that sets up and cleans up something tied to one component instance is not a violation.
