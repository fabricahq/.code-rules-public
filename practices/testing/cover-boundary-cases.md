---
title: "Cover empty inputs and boundaries"
whenToRead: "Before planning, writing, changing, or reviewing code or tests that process collections, check ranges or thresholds, compute positions, or relate two items, such as validation limits, pagination, sorting, or moving items in a list or tree."
impact: "MEDIUM"
impactDescription: "Catches bugs at the edges, which tests that use only ordinary inputs never reach."
tags: "testing"
---

## Cover empty inputs and boundaries

Test each input the contract treats differently: empty and single-item collections, first and last positions, exact thresholds, and an item related to itself. Assert the intended result for each case.

Bugs often cluster at these edges because each one takes a different path through the code. Edge cases fail in three ways: a crash, a misleading error, or a silently wrong result. A test that only checks for "no crash" misses the last two.

Cover each boundary at the lowest test layer that can prove it, usually a unit test. Do not repeat edge-case variants in UI or end-to-end tests unless the boundary exists only at that layer. Keep each case cheap: a table-driven or parameterized test can hold one row per boundary. Be most thorough where a wrong edge result loses or corrupts data.

**Incomplete:** a function accepts retry counts from 1 through 3, and the only test uses 2.

**Complete:** tests for 0, 1, 3, and 4, each asserting the documented acceptance or error. 1 and 3 prove the inclusive bounds, and 0 and 4 prove the rejections. 2 sits inside the documented range, so it proves nothing 1 and 3 do not.

**Incomplete:** a function that moves an item before a target item in a list is tested only by reordering three distinct items.

**Complete:** also move an item before itself, move the only item in a list, and move items to the first and last positions. If the function removes the item before looking up the target, moving an item before itself fails with a misleading "target not found" error that the three-item test never reaches.

Where to look for cases:

- **Collections:** empty and single-item inputs. An empty input often means there is nothing to loop over or renumber, and a single item skips the logic that runs between items.
- **Positions and thresholds:** the first slot, the last slot, and the values just on each side of every threshold. This is where `<` versus `<=` mistakes hide.
- **Relationships:** the same item on both sides, and a missing counterpart. For "is folder A inside folder B," test A inside A, and a root folder that has no parent.

**When the intended result is unclear:** edge cases often show that the contract never decided. Is a folder inside itself? Decide, write the answer into the function's contract, enforce it in the implementation, and write a test that checks that enforcement.

### Validation

List the boundaries the contract defines and match each one to a test that asserts the intended result. Use the implementation to find boundaries the contract leaves implicit, but choose and assert cases through the interface callers use, so that refactoring the implementation does not break the tests.

A missing case is not a gap when it takes the same path as a tested case, such as another value inside a range whose bounds are already tested. It is also not a gap when the contract or type system rules the input out, such as an empty list passed to a function that only accepts a non-empty type.

When an edge-case bug gets past the tests, reproduce it with a failing test before fixing it, and keep that test.
