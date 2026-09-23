---
title: "Reproduce bugs with regression tests"
whenToRead: "When diagnosing and fixing a reproducible behavior defect."
impact: "HIGH"
impactDescription: "Prevents a fixed bug from returning unnoticed in a later change."
tags: "testing"
---

## Reproduce bugs with regression tests

Before fixing a reproducible bug, write a test that triggers the reported failure and run it against the unfixed behavior. Confirm it fails for the reported reason, apply the fix, and keep the passing test with the change.

Choose the lowest layer that faithfully reproduces the bug through an interface callers use. Use a UI or integration test when a unit test cannot reproduce the failure. Do not force a pure-function extraction solely to satisfy this rule.

**Incorrect:** fix case-insensitive sorting, then add a test containing only lowercase names. It would pass before the fix and does not guard the bug.

**Correct:** sort `alpha`, `Beta`, and `gamma`; expect `alpha`, `Beta`, `gamma`. A case-sensitive comparison puts `Beta` first. Confirm the test fails with the old comparison and passes with the intended comparison.

For an urgent fix where a reliable reproduction is not yet possible, record what was verified and the remaining coverage gap. Do not claim a passing-after-only test proves the regression was reproduced.

Background: [Testing philosophy](../../assets/testing-philosophy.md).

### Validation

Keep evidence that the test fails for the original symptom before the fix and passes after it. Verify related valid inputs still work. Name the test for the behavior, not a private helper or incident number.
