# Testing philosophy

This page explains the reasoning behind the rules in the Testing group.
It is background only: each rule states its own obligations, exceptions, and checks.

## Speed is limited by safety

Automated tests work like a car's brakes.
A car can drive fast only because it can stop, and a team can change code quickly only when its tests stop a defect before it reaches users.
Without tests, software is broken until someone proves it works.
With a test suite that runs on every change, each change proves the software still works, and the team learns the moment it breaks.

This framing follows Yevgeniy Brikman's essay [Agility Requires Safety](https://www.ybrikman.com/writing/2016/02/14/agility-requires-safety/).

## The build tests itself

Every change runs the automated checks and tests before it merges.
A failing build is fixed quickly or the change that broke it is reverted, never left failing.
Small, frequent changes keep each failure easy to locate and undo.

## What to test is a trade-off

Testing effort is limited, so spend it where it prevents the most harm.
Three factors decide where:

- **Likelihood of bugs:** higher in complex logic, such as parsing, state lifecycles, tree and graph building, synchronization, and calculations, than in declarative wiring or simple delegation.
- **Cost of bugs:** higher where users can lose or corrupt data, where security or permissions are involved, where an action cannot be undone, or where two implementations of the same contract can silently drift apart.
- **Cost of tests:** unit tests are cheap to write and run, integration tests cost more, and end-to-end tests through a user interface cost the most to write, run, and maintain.

## Tests are code

Every test has a maintenance cost.
A test earns its place when it would fail on a plausible real regression.
Tests that restate the implementation, retest a framework, or exist only to raise a coverage number cost time without adding safety.
When a type system, schema, or generated-output check can rule out a whole class of bug, it is usually cheaper and more reliable than many handwritten tests.

## The test ladder

Test layers form a ladder from cheapest to most expensive: unit, integration, and end-to-end.
A behavior belongs on the lowest rung that can actually prove it.
Most tests end up as unit tests, some as integration tests, and a few as end-to-end tests that cover critical journeys.
A lower rung is not always enough: a fake can only prove what the fake does, so behavior enforced by a real database, file system, or browser needs a test that includes it.

## Tests survive refactoring

Tests that assert what callers and users observe stay valid when the implementation changes.
If a behavior-preserving refactor breaks many tests, those tests were checking implementation details.
