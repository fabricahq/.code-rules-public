---
title: "Avoid loading large barrel files"
whenToRead: "Before planning, writing, changing, or reviewing imports from large packages that re-export many modules through one entry file, such as icon and component libraries, or when diagnosing slow development builds or cold starts."
impact: "MEDIUM"
impactDescription: "Importing from a large barrel file can load thousands of unused modules when the toolchain cannot eliminate them, slowing builds and cold starts."
tags: "react, bundling, imports, nextjs"
attribution:
  - url: https://github.com/vercel-labs/agent-skills/blob/4ec6f84b61cd3c931046c3e6e398f3ae7de372f7/skills/react-best-practices/rules/bundle-barrel-imports.md
    description: "Adapted from the Vercel Agent Skills rule bundle-barrel-imports: restructured to the rule template, recalibrated impact, and labeled measurements as reported by the source."
---

## Avoid loading large barrel files

When a package's entry file re-exports many modules, make sure only the modules you use are loaded.
Use the framework's import optimization when available, or import from the specific module path.

### Implementation

- In Next.js, list the package in `optimizePackageImports`, which rewrites barrel imports to direct imports at build time and keeps the ordinary import syntax.
- Without such an optimization, import from the specific module path, such as `@mui/material/Button`.
  Check that the package publishes types for those paths; some packages do not, which produces implicit `any` under strict settings.
- Measure development startup, build time, or cold start before and after the change.
  The benefit depends on the package's structure, the bundler, and whether the package is bundled or treated as external.
- Your own small internal barrels are rarely the problem; focus on third-party packages with hundreds or thousands of exports.

### Rationale

A barrel file re-exports every module in a package.
When the toolchain cannot tree-shake it, such as a package loaded unbundled in development or on the server, importing one name evaluates every re-exported module.
Vercel reported that importing a few icons from one popular icon library loaded about 1,500 modules and added seconds to development startup.

### Examples

**Incorrect (counterexample):**

```tsx
import { Button, TextField } from '@mui/material';
```

Without an import optimization, this can load the whole component library.

**Correct (Next.js):**

```js
// next.config.js
module.exports = {
  experimental: {
    optimizePackageImports: ['@mui/material'],
  },
};
```

```tsx
import { Button, TextField } from '@mui/material';
```

**Correct (without a framework optimization):**

```tsx
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
```

### Validation

Measure module count or startup time before and after the change, and keep it only if it helps.
Check that direct import paths type-check under the project's settings.

A barrel import from a package the toolchain already optimizes is not a violation.
