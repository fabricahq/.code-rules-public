---
title: "Say what the product is before anything else"
whenToRead: "Before writing or reviewing the opening of a README, such as its title, tagline, first paragraph, badges, and any notices or links placed above the description."
impact: "MEDIUM"
impactDescription: "Readers who cannot tell what a product is from the first screen leave or misjudge it, and those who stay follow setup steps without knowing whether the product fits their needs."
tags: "documentation, readme"
---

## Say what the product is before anything else

Open the README with a plain statement of what the product is, what it acts on, and the problem it solves.
Put nothing before that statement that assumes the reader already knows the product, such as install steps, notices, pointers to the documentation, or tables.

### Implementation

- Name a category the reader already knows, such as "a command-line tool that…", "a GitHub Action that…", or "a Go library for…".
  An analogy to a familiar tool helps when it is accurate.
- Say what the product acts on and what the reader gets, in concrete terms.
- Name hard constraints that decide whether a reader can use it, such as supported platforms, required services, or a hosting provider, in the opening paragraph or directly after it.
- For a primary product, the tagline and promise make this statement.
  For a secondary product, the first sentence of the opening paragraph makes it.
- A short status notice, such as a pre-release warning, can come directly after the statement.

### Examples

**Incorrect (counterexample):**

```md
# Shipwright

The full documentation is in [`docs/`](docs/), a site you can run locally.

## Overview

Shipwright streamlines your delivery lifecycle with intelligent automation.
```

The first line is about where the documentation lives, and the overview does not say what Shipwright does or what it works with.

**Correct:**

```md
# Shipwright

Shipwright deploys container images to Fly.io from GitHub Actions and rolls back automatically when health checks fail.
It works with GitHub only.
```

### Validation

Read only the title and the opening paragraph, or the title block for a primary product.
Someone unfamiliar with the product should be able to answer three questions: what kind of thing is it, what does it act on, and can I use it in my setup?

Badges above the statement are not a violation.
Neither is a link to the documentation after the statement.
