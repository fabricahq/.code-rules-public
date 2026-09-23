---
title: "Use Fast Focused Test Tooling"
whenToRead: "Before choosing how to run or debug one TypeScript unit, integration, or browser test."
impact: "LOW"
impactDescription: "encourages fast single-test feedback loops during implementation and debugging"
tags: "typescript, testing, vitest, playwright, tooling, feedback-loop"

attribution:
  - url: "https://github.com/mkosir/typescript-style-guide/blob/86bebd58a987e23277dba02028c0ee2d6ffb5073/website/src/pages/index.mdx"
    description: "Underlying TypeScript Style Guide material; required notice is retained in NOTICE.md."
---

## Use Fast Focused Test Tooling

Run the smallest relevant test during implementation and debugging so the
feedback identifies one behavior quickly. A test runner's single-file or
single-test command works in any editor. Editor integrations such as [Vitest Runner](https://marketplace.visualstudio.com/items?itemName=vitest.explorer) and [Playwright Test](https://marketplace.visualstudio.com/items?itemName=ms-playwright.playwright) can make this faster when the project uses those tools. They are optional conveniences, not a requirement to use VS Code.

For example, run one named Vitest test or one Playwright spec while changing
its behavior, then run the wider project checks before completing the change.
A focused pass only establishes that the selected test passes; it does not
replace the broader suite.
