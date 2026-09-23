---
title: "Use Named Exports"
whenToRead: "Before choosing or reviewing TypeScript module exports and imports."
impact: "LOW"
impactDescription: "keeps imports uniform and lets missing exported names fail clearly"
tags: "typescript, exports, named-exports, imports, consistency"

attribution:
  - url: "https://github.com/mkosir/typescript-style-guide/blob/86bebd58a987e23277dba02028c0ee2d6ffb5073/website/src/pages/index.mdx"
    description: "Underlying TypeScript Style Guide material; required notice is retained in NOTICE.md."
---

## Use Named Exports

**Related automated rule:** Named exports must be used to ensure that all imports follow a uniform pattern [Reference](https://github.com/import-js/eslint-plugin-import/blob/main/docs/rules/no-default-export.md)

```js
'import/no-default-export': 'error'

// In case of exceptions disable the rule
overrides: [
    {
      files: ["src/pages/**/*"],
      rules: { "import/no-default-export": "off" },
    }
]
```

This keeps variables, functions etc. names consistent across the entire codebase. Named exports have the benefit of
erroring when import statements try to import something that hasn't been declared.
