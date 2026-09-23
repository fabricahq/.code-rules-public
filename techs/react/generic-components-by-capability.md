---
title: "Name generic components by capability, not by first caller"
whenToRead: "Before naming, extracting, moving, or reviewing a reusable React component, especially one first written for a single feature."
impact: "MEDIUM"
impactDescription: "A generic component named after its first feature discourages reuse and attracts feature-specific logic until the false coupling becomes real."
tags: "react, naming, components"
---

## Name generic components by capability, not by first caller

Name a generic component for the capability it provides, such as `InlineDisclosure`, not for the feature that first needed it, such as `BillingDisclosure`.
Keep domain names for components that are genuinely specific to that domain.

### Implementation

Apply the strip-the-domain-word test: if the name still makes sense without the product or feature word, the component is generic and should not carry that word.
Then choose one of three fixes:

- **The wrapper adds nothing:** delete it and use the underlying primitive directly.
- **The wrapper adds reusable defaults,** such as styling, icon placement, accessibility attributes, or state conventions: rename it for the capability and place it with shared components when it is reused.
- **The helper exists only to keep repeated markup readable inside one feature file:** it may keep a feature-scoped name while it stays private to that file.
  Rename it when it is exported or moved.

Also:

- Avoid layout qualifiers such as `Sidebar` or `Modal` when the component is not specific to that surface.
- Role words such as `Section`, `Panel`, and `Page` are fine for feature components.
- A capability name does not require moving the component; move it to shared components when a second caller appears or it is clearly part of the shared UI.

### Rationale

A name tells future readers where a component belongs and whether they may reuse it.
A feature name on a generic component makes other features copy it instead of reusing it, and invites feature-specific props until the component really is coupled to the feature.

### Examples

#### Application: A wrapper that adds nothing

**Incorrect (counterexample):**

```tsx
function BillingCollapsible({ children }: { children: ReactNode }) {
  return <Collapsible>{children}</Collapsible>;
}
```

**Correct:**

```tsx
<Collapsible>{children}</Collapsible>
```

#### Application: A wrapper with reusable defaults

**Incorrect (counterexample):**

```tsx
export function BillingDisclosure({ title, children, open, onOpenChange }: DisclosureProps) {
  return (
    <Collapsible open={open} onOpenChange={onOpenChange}>
      <CollapsibleTrigger>{title}</CollapsibleTrigger>
      <CollapsibleContent>{children}</CollapsibleContent>
    </Collapsible>
  );
}
```

Nothing about the component is specific to billing.

**Correct:**

```tsx
export function InlineDisclosure({ title, children, open, onOpenChange }: DisclosureProps) {
  return (
    <Collapsible open={open} onOpenChange={onOpenChange}>
      <CollapsibleTrigger>{title}</CollapsibleTrigger>
      <CollapsibleContent>{children}</CollapsibleContent>
    </Collapsible>
  );
}
```

### Validation

For each new or renamed exported component, apply the strip-the-domain-word test.

A component that renders domain data or behavior, such as `CustomerDetailPage`, is not a violation, and neither is a private helper inside one feature file.
