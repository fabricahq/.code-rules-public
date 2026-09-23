---
title: "Create explicit component variants instead of boolean mode props"
whenToRead: "Before planning, writing, changing, or reviewing a React component that selects substantially different layouts or behavior through boolean props, such as isEditing, isThread, or isCompact."
impact: "MEDIUM"
impactDescription: "Each boolean mode prop multiplies the combinations a component must handle, including impossible ones, and buries each variant in conditionals."
tags: "react, composition, components, props"
attribution:
  - url: https://github.com/vercel-labs/agent-skills/tree/4ec6f84b61cd3c931046c3e6e398f3ae7de372f7/skills/composition-patterns/rules
    description: "Adapted from two Vercel Agent Skills rules (architecture-avoid-boolean-props and patterns-explicit-variants): merged two overlapping rules on boolean props and explicit variants, restructured to the rule template, and recalibrated impact."
---

## Create explicit component variants instead of boolean mode props

When boolean props select different modes of a component, create a separate component for each mode that composes shared parts.

### Implementation

- Identify the modes the booleans represent, such as a thread composer, an edit composer, and a forward composer.
- Build shared parts, such as a frame, input, and footer, and write one component per mode that composes the parts it needs.
- Move mode-specific data and actions into that mode's component or provider.
- A boolean that toggles one small, independent detail, such as `disabled` or `showIcon`, can stay a boolean.

### Rationale

Every boolean doubles the combinations a component can receive, and many combinations, such as editing while forwarding, are meaningless.
The component then fills with nested conditionals, and readers must trace them to learn what a given call renders.
Explicit variants make each mode's structure visible and let impossible combinations disappear.

### Examples

**Incorrect (counterexample):**

```tsx
function Composer({ isThread, isEditing, isForwarding, channelId, messageId }: ComposerProps) {
  return (
    <form>
      <Input />
      {isThread ? <AlsoSendToChannelField id={channelId} /> : null}
      {isEditing ? <EditActions messageId={messageId} /> : isForwarding ? <ForwardActions /> : <SubmitButton />}
    </form>
  );
}

<Composer isThread isEditing={false} channelId="abc" />;
```

Readers cannot tell what a call renders without tracing every flag, and the props allow editing and forwarding at once.

**Correct:**

```tsx
function ThreadComposer({ channelId }: { channelId: string }) {
  return (
    <ComposerFrame>
      <ComposerInput />
      <AlsoSendToChannelField id={channelId} />
      <ComposerSubmit />
    </ComposerFrame>
  );
}

function EditMessageComposer({ messageId }: { messageId: string }) {
  return (
    <ComposerFrame>
      <ComposerInput />
      <EditActions messageId={messageId} />
    </ComposerFrame>
  );
}
```

Each variant states what it renders, and shared parts keep the variants consistent.

### Validation

Count the boolean props on components that switch layouts or behavior.
When two or more of them select mutually exclusive modes, the component should be split into variants.

An independent boolean that toggles one detail is not a violation.
