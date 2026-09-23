---
title: "Prefer Single Object Function Args"
whenToRead: "Before designing a TypeScript function with several related arguments or evolving call sites."
impact: "LOW"
impactDescription: "keeps multi-parameter calls readable and easier to extend safely"
tags: "typescript, functions, arguments, options-object, readability"

attribution:
  - url: "https://github.com/mkosir/typescript-style-guide/blob/86bebd58a987e23277dba02028c0ee2d6ffb5073/website/src/pages/index.mdx"
    description: "Underlying TypeScript Style Guide material; required notice is retained in NOTICE.md."
---

## Prefer Single Object Function Args

To keep function readable and easily extensible for the future (adding/removing args), strive to have single object as the function arg, instead of multiple args.
 As an exception this does not apply when having only one primitive single arg (e.g. simple functions isNumber(value), implementing currying etc.).

```ts
// Avoid having multiple arguments
transformUserInput('client', false, 60, 120, null, true, 2000);

// Use options object as argument
transformUserInput({
  method: 'client',
  isValidated: false,
  minLines: 60,
  maxLines: 120,
  defaultInput: null,
  shouldLog: true,
  timeout: 2000,
});
```
