---
title: "Name Generic Components by Capability, Not by First Caller"
whenToRead: "Before naming a reusable React component first created for one feature."
impact: "MEDIUM"
impactDescription: "keeps reusable generic components discoverable without coupling them to their first use case"
tags: "react, naming, components, reuse, composition, abstraction, wrappers, capability, domain-names"
---

## Name Generic Components by Capability, Not by First Caller

Name a generic component for the capability it provides, not for the feature
that first needed it. A first-caller name such as `FeatureDisclosure` quietly
claims "this belongs to one feature" even when the component only provides a
generic disclosure treatment. That discourages reuse, and it invites future
callers to pour feature-specific behavior into the component until the name's
false coupling becomes true.

Semantic feature components can keep domain names, while generic capabilities should not inherit the first caller's domain word.

## Choose the Fix

First-caller names usually point to one of three different fixes.

### 1. No extra value: delete the wrapper

If the component only passes through a primitive, the problem is unnecessary
indirection. Delete the wrapper and use the primitive directly.

```tsx
// Incorrect: the wrapper adds no defaults or feature meaning.
function FeatureCollapsible({ children }: { children: ReactNode }) {
  return <Collapsible>{children}</Collapsible>;
}

// Correct: use the primitive directly.
<Collapsible>{children}</Collapsible>;
```

### 2. Reusable defaults: rename by capability

If the wrapper adds real defaults - styling, icon placement, spacing,
accessibility affordances, or state conventions - and that treatment is reusable,
name it for the capability and place it where shared components live.

```tsx
// Incorrect: exported shared treatment named for its first caller.
export function FeatureDisclosure({
  title,
  children,
  open,
  onOpenChange,
}: DisclosureProps) {
  return (
    <Collapsible open={open} onOpenChange={onOpenChange}>
      <CollapsibleTrigger>{title}</CollapsibleTrigger>
      <CollapsibleContent>{children}</CollapsibleContent>
    </Collapsible>
  );
}
```

```tsx
// Correct: capability name in shared components.
export function InlineDisclosure({
  title,
  children,
  open,
  onOpenChange,
}: DisclosureProps) {
  return (
    <Collapsible open={open} onOpenChange={onOpenChange}>
      <CollapsibleTrigger>{title}</CollapsibleTrigger>
      <CollapsibleContent>{children}</CollapsibleContent>
    </Collapsible>
  );
}
```

### 3. Private local repetition: keep it local

This rule does not ban small private helpers inside a feature file. A file-local
helper may combine the feature scope with a capability name
(`FeaturePromptDisclosure`) when it exists only to keep repeated local markup
readable and is not exported as a reusable abstraction. If that helper moves out
of the feature file or becomes shared, rename it to the generic capability and
place it with shared components.

## Guidelines

- Apply the strip-the-domain-word test: "If I removed the product/domain word
  from the name, would the component still make sense?" If yes, the component is
  generic and should not be named for that domain. If no, the component is
  genuinely coupled to the domain (`CustomerNavigator`, `CustomerDetailPage`)
  and should keep the product name.
- A capability name alone is not a mandate to relocate. Promote to shared when
  reuse is real, when a second caller appears, or when the capability is
  obviously generic and intentionally part of the shared UI surface.
- A thin wrapper whose only job is to supply styling/props to a generic
  primitive is usually capability-named, not content-named. The exception is a
  private file-local helper that scopes a repeated feature treatment without
  promising reuse outside the file.
- Avoid location/layout qualifiers (`Sidebar...`, `Modal...`, `LeftPanel...`)
  when the component is not actually specific to that surface.
- `Section`, `Panel`, and `Page` are legitimate role terms for semantic feature components. This rule applies when the component is generic but was named after its first caller.
