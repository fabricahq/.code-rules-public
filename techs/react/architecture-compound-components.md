---
title: "Build complex components from composable parts"
whenToRead: "Before planning, writing, changing, or reviewing a React component with several optional or rearrangeable parts, such as a composer, card, or dialog configured through show flags or render props."
impact: "MEDIUM"
impactDescription: "Monolithic components configured through flags and render props grow a prop for every new arrangement and are hard for callers to read."
tags: "react, composition, compound-components, children"
attribution:
  - url: https://github.com/vercel-labs/agent-skills/blob/4ec6f84b61cd3c931046c3e6e398f3ae7de372f7/skills/composition-patterns/rules/architecture-compound-components.md
    description: "Adapted from the Vercel Agent Skills rule architecture-compound-components: merged with the children-over-render-props rule, restructured to the rule template, and recalibrated impact."
  - url: https://github.com/vercel-labs/agent-skills/blob/4ec6f84b61cd3c931046c3e6e398f3ae7de372f7/skills/composition-patterns/rules/patterns-children-over-render-props.md
    description: "Adapted from the Vercel Agent Skills rule patterns-children-over-render-props: merged with the children-over-render-props rule, restructured to the rule template, and recalibrated impact."
---

## Build complex components from composable parts

Structure a component with optional or rearrangeable parts as a set of compound components that callers compose as children, sharing state through context.
Use render props only when the component must pass data back to the caller's content.

### Implementation

- Export the parts together, such as `Composer.Frame`, `Composer.Input`, and `Composer.Submit`, and let callers arrange them as children.
- Share state and actions among the parts through a context provided by the root or a provider component, instead of threading props through every part.
- Replace `showX` flags and `renderX` props for static structure with children.
- Keep a render prop, such as `renderItem`, when the component supplies data to each piece of caller content.

### Rationale

A monolithic component needs a new prop for every optional part and every arrangement callers want.
Callers then configure structure indirectly through flags and callbacks.
With composable parts, callers write the structure they want directly, and adding a part does not change the existing API.

### Examples

#### Application: Optional parts

**Incorrect (counterexample):**

```tsx
<Composer
  showAttachments
  showFormatting={false}
  renderHeader={() => <CustomHeader />}
  renderActions={() => <SubmitButton />}
/>
```

**Correct:**

```tsx
<Composer.Provider state={state} actions={actions}>
  <Composer.Frame>
    <CustomHeader />
    <Composer.Input />
    <Composer.Footer>
      <Composer.Attachments />
      <Composer.Submit />
    </Composer.Footer>
  </Composer.Frame>
</Composer.Provider>
```

Callers see and control exactly which parts appear and in what order.

#### Application: Content that needs data from the component

**Correct:**

```tsx
<List items={items} renderItem={(item) => <ItemRow item={item} />} />
```

The list supplies each item, so a render prop is the right tool.

### Validation

Check components with several `showX` or `renderX` props for static structure; they should expose composable parts instead.

A render prop that receives data from the component is not a violation.
