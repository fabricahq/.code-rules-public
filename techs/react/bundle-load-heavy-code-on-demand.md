---
title: "Load heavy optional code on demand"
whenToRead: "Before planning, writing, changing, or reviewing React code that imports large components, libraries, or data used only after a user action or when a feature is enabled, such as an editor, chart library, or animation data."
impact: "HIGH"
impactDescription: "Heavy code that most visits never use enlarges the initial bundle and delays the first interaction for every user."
tags: "react, bundling, code-splitting, lazy, dynamic-import"
attribution:
  - url: https://github.com/vercel-labs/agent-skills/blob/4ec6f84b61cd3c931046c3e6e398f3ae7de372f7/skills/react-best-practices/rules/bundle-dynamic-imports.md
    description: "Adapted from the Vercel Agent Skills rule bundle-dynamic-imports: merged three rules on dynamic imports, conditional loading, and intent-based preloading, restructured to the rule template, and recalibrated impact."
  - url: https://github.com/vercel-labs/agent-skills/blob/4ec6f84b61cd3c931046c3e6e398f3ae7de372f7/skills/react-best-practices/rules/bundle-conditional.md
    description: "Adapted from the Vercel Agent Skills rule bundle-conditional: merged three rules on dynamic imports, conditional loading, and intent-based preloading, restructured to the rule template, and recalibrated impact."
  - url: https://github.com/vercel-labs/agent-skills/blob/4ec6f84b61cd3c931046c3e6e398f3ae7de372f7/skills/react-best-practices/rules/bundle-preload.md
    description: "Adapted from the Vercel Agent Skills rule bundle-preload: merged three rules on dynamic imports, conditional loading, and intent-based preloading, restructured to the rule template, and recalibrated impact."
---

## Load heavy optional code on demand

Load large components, libraries, and data that the first screen does not need with a dynamic import, such as `React.lazy`, `next/dynamic`, or `import()`, when the user needs them.
Start loading early when the user signals intent, so the wait is short.

### Implementation

- Wrap heavy optional components with `React.lazy` and a `Suspense` fallback, or with the framework's equivalent, such as `next/dynamic`.
- Load large libraries or data with `import()` inside the event handler or code path that needs them.
- Start the import on intent signals, such as hover or focus on the button that opens the feature, or when a feature flag enables it.
- In Next.js, `ssr: false` works only inside Client Components.
- Keep code in the main bundle when the first screen renders it; lazy-loading it adds a request and a fallback without saving anything.
- Check the build output or bundle analyzer to confirm the code moved to a separate chunk.

### Rationale

Everything in the initial bundle must be downloaded, parsed, and executed before the page is interactive.
Code that only some users reach, after an action, makes every user pay that cost up front.
Loading it on demand moves the cost to the users who need it, and preloading on intent hides most of the wait.

### Examples

#### Application: A heavy component behind a user action

**Incorrect (counterexample):**

```tsx
import { MonacoEditor } from './monaco-editor';

function CodePanel({ code, isOpen }: { code: string; isOpen: boolean }) {
  return isOpen ? <MonacoEditor value={code} /> : null;
}
```

Every visitor downloads the editor, even those who never open the panel.

**Correct:**

```tsx
const MonacoEditor = lazy(() => import('./monaco-editor').then((module) => ({ default: module.MonacoEditor })));

function preloadEditor() {
  void import('./monaco-editor');
}

function CodePanel({ code, isOpen }: { code: string; isOpen: boolean }) {
  return isOpen ? (
    <Suspense fallback={<EditorSkeleton />}>
      <MonacoEditor value={code} />
    </Suspense>
  ) : null;
}

function OpenEditorButton({ onOpen }: { onOpen: () => void }) {
  return (
    <button onClick={onOpen} onMouseEnter={preloadEditor} onFocus={preloadEditor}>
      Open editor
    </button>
  );
}
```

The editor loads when the panel opens, and hovering or focusing the button starts the download early.

### Validation

Inspect the bundle analyzer output and check that the heavy module is in its own chunk and not in the initial one.
In the network panel, check that the chunk loads only after the triggering action or intent signal.

Code rendered on the first screen that stays in the main bundle is not a violation.
