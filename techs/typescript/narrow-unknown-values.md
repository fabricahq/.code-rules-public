---
title: "Narrow unknown values before use"
whenToRead: "When handling external data or values whose runtime shape is not yet established."
impact: "HIGH"
impactDescription: "Prevents unchecked data from bypassing TypeScript and failing later at runtime."
tags: "typescript"
attribution: [{"url": "https://github.com/josh-padnick/code-rules/blob/0621607fae1ed732a2ec90d9bbe906bc5a4ecf78/typescript/use-unknown-instead-of-any.md", "description": "Adapted for public reuse: added reading guidance, simplified examples, and removed repository-specific assumptions."}, {"url": "https://github.com/mkosir/typescript-style-guide/blob/86bebd58a987e23277dba02028c0ee2d6ffb5073/website/src/pages/index.mdx", "description": "Underlying TypeScript Style Guide material by mkosir, adapted under MIT; copyright and permission notice retained in NOTICE.md."}]
---

## Narrow unknown values before use

Use `unknown` for data whose shape has not been established, then validate it before accessing properties or assigning it to a narrower type. Avoid `any` at these boundaries because it disables the checks that would require that validation.

**Incorrect:** a cast changes the compiler's belief without validating the value.

```ts
const value: unknown = JSON.parse(responseText);
const count = value as number;
```

**Correct:** a runtime check establishes the type before use.

```ts
const value: unknown = JSON.parse(responseText);
if (typeof value !== 'number' || !Number.isFinite(value)) {
  throw new Error('Expected a finite numeric count');
}
const count = value;
```

Validate the domain constraints as well: a numeric value may still be invalid as a count. Use an existing schema validator when it owns that boundary. Where an external library forces `any`, contain it at the adapter and return validated types.

### Validation

Inspect data entry points and verify that property access follows runtime validation. Include malformed-input tests. Replacing `any` with an unchecked assertion does not satisfy this rule.
