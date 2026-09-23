---
title: "Model distinct states as discriminated unions"
whenToRead: "Before planning, writing, changing, or reviewing TypeScript types or code for values that can be in one of several states with different data, such as operation results, loading states, or events with kind-specific fields."
impact: "MEDIUM"
impactDescription: "Makes impossible field combinations harder to construct and missing cases easier to detect."
tags: "typescript"
attribution: [{"url": "https://github.com/mkosir/typescript-style-guide/blob/86bebd58a987e23277dba02028c0ee2d6ffb5073/website/src/pages/index.mdx", "description": "Underlying TypeScript Style Guide material by mkosir, adapted under MIT; copyright and permission notice retained in NOTICE.md."}]
---

## Model distinct states as discriminated unions

Represent mutually exclusive states as a union of object types that share a literal discriminator property.
Keep each state's required data in its own variant instead of making every field optional on one type.

### Implementation

- Give every variant the same discriminator property, such as `kind` or `status`, with a distinct string literal value.
- Make each variant's fields required when the state requires them, and leave out fields that do not apply to that state.
- Narrow on the discriminator before reading variant-specific fields.
- When code must handle every variant, make the compiler report a missing case.
  Assign the value to `never` in the `default` branch, or use the project's exhaustive-switch lint rule.
- Do not add a `default` branch that silently handles unknown variants in code that must handle every variant.

A truly independent on/off option can remain a boolean.
It does not need a state model unless it combines with other fields into states that exclude each other.

### Rationale

A single type with optional fields lets the compiler accept combinations the program never intends, such as a success with no data or a result with both data and an error.
Every reader must then check which fields are present and guess what each combination means.
A discriminated union makes each valid state explicit, lets TypeScript narrow to the fields that exist in that state, and turns a newly added state into a compile error wherever code must handle it.

### Examples

#### Application: Modeling mutually exclusive states

An operation either succeeds with data or fails with an error message.

**Incorrect (counterexample):**

```ts
type Result = { success: boolean; data?: string; error?: string };
```

The type permits a success without data, a failure without an error, and a value with both.

**Correct:**

```ts
type Result =
  | { kind: 'success'; data: string }
  | { kind: 'failure'; error: string };
```

Each state has exactly the fields its contract requires.

#### Application: Handling every state

A `pending` state is later added to the `Result` union, and a function formats results for display.

**Incorrect (counterexample):**

```ts
function describe(result: Result): string {
  switch (result.kind) {
    case 'success':
      return result.data;
    case 'failure':
      return result.error;
    default:
      return 'Unknown';
  }
}
```

The `default` branch compiles after `pending` is added, so pending results silently display as `Unknown`.

**Correct:**

```ts
function describe(result: Result): string {
  switch (result.kind) {
    case 'success':
      return result.data;
    case 'failure':
      return result.error;
    default: {
      const unhandled: never = result;
      throw new Error(`Unhandled result: ${JSON.stringify(unhandled)}`);
    }
  }
}
```

Adding `pending` makes the assignment to `never` fail to compile, which points to the case that needs handling.

#### Application: An independent option

A search request has an option that includes archived items.

**Correct:**

```ts
type SearchRequest = { query: string; includeArchived: boolean };
```

The option does not exclude any other field or change which fields are required, so a boolean is enough.

### Validation

Try constructing a success without data and a failure without an error; the compiler should reject both.
Add a temporary new variant and check that every consumer that must handle all variants reports the missing case.

A boolean or optional field is not a violation when it is independent of the other fields.
A `default` branch is not a violation in code that intentionally handles only some variants, such as a filter for one state.
