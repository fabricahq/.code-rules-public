---
title: "Express operations as meaningful steps"
whenToRead: "When a function mixes orchestration with parsing, validation, or normalization details."
impact: "MEDIUM"
impactDescription: "Helps readers understand the operation without tracing every implementation detail."
tags: "code-design"
---

## Express operations as meaningful steps

Express an operation as a sequence of meaningful steps at a consistent level of abstraction.
Put detailed parsing and validation behind named helpers when their contracts let readers understand the caller without inspecting their implementations.
A helper earns its place by centralizing an invariant or hiding a meaningful operation, not merely by reducing line count.

Apply this rule when a function mixes orchestration with nested parsing, field validation, normalization, or error construction that obscures the overall operation.
A short, cohesive function does not need extraction merely because it could be divided into smaller functions.

This is a language-independent practice for function and module design.
The TypeScript examples illustrate the structure; apply the same principle in other languages.

### Example

Both versions below load an export manifest, validate its declared file paths, check that the files exist, and return unique paths in code-unit order.
The examples use the same existing validation utilities: `object` rejects non-objects, `nonempty` rejects non-string or blank values, `relativePath` rejects paths escaping the source root, and `requiredFile` rejects missing files.
Each utility reports errors at the supplied location.
These are excerpts from a module importing those utilities.

**Incorrect** - manifest interpretation and per-field validation obscure the operation's overall steps:

```ts
/** Return unique declared export paths in code-unit order; reject invalid manifests or missing files. */
export function collectExportPaths(
  sourceFiles: ReadonlyMap<string, string>,
): ReadonlyArray<string> {
  const manifest = object(
    JSON.parse(requiredFile(sourceFiles, 'exports.json', 'library')),
    'exports.json',
  );
  const values = manifest.files;
  if (!Array.isArray(values)) {
    throw new Error('exports.json: files must be an array');
  }
  const entries: ReadonlyArray<unknown> = values;
  const declarations = entries.map((value, index) => {
    const location = `exports.json: files[${index}]`;
    return {
      path: relativePath(nonempty(value, location), location),
      location,
    };
  });
  for (const { path, location } of declarations) {
    requiredFile(sourceFiles, path, location);
  }
  return [...new Set(declarations.map(({ path }) => path))].sort();
}
```

**Correct** - the caller names the domain steps, while private helpers own their details:

```ts
/** A source-relative path paired with the manifest field that declared it. */
type DeclaredPath = {
  readonly path: string;
  readonly location: string;
};

/** Return unique declared export paths in code-unit order; reject invalid manifests or missing files. */
export function collectExportPaths(
  sourceFiles: ReadonlyMap<string, string>,
): ReadonlyArray<string> {
  const manifest = exportManifest(sourceFiles);
  const declarations = exportDeclarations(manifest);
  requireDeclaredFiles(sourceFiles, declarations);
  return [...new Set(declarations.map(({ path }) => path))].sort();
}

/** Load exports.json as an object; reject a missing file, invalid JSON, or a non-object value. */
function exportManifest(
  sourceFiles: ReadonlyMap<string, string>,
): Record<string, unknown> {
  const text = requiredFile(sourceFiles, 'exports.json', 'library');
  const value: unknown = JSON.parse(text);
  return object(value, 'exports.json');
}

/** Validate declared export paths in input order, retaining duplicates and indexed error locations. */
function exportDeclarations(
  manifest: Record<string, unknown>,
): ReadonlyArray<DeclaredPath> {
  const values = manifest.files;
  if (!Array.isArray(values)) {
    throw new Error('exports.json: files must be an array');
  }
  const entries: ReadonlyArray<unknown> = values;
  return entries.map((value, index) => {
    const location = `exports.json: files[${index}]`;
    const text = nonempty(value, location);
    return { path: relativePath(text, location), location };
  });
}

/** Reject the first declaration whose path is absent from the source files. */
function requireDeclaredFiles(
  sourceFiles: ReadonlyMap<string, string>,
  declarations: ReadonlyArray<DeclaredPath>,
): void {
  for (const { path, location } of declarations) {
    requiredFile(sourceFiles, path, location);
  }
}
```

The direct mapping and final sort remain inline because their behavior is apparent at the call site.
The helpers describe domain operations; names such as `stepOne` or `processData` would add navigation without helping readers understand the caller.

### Guidelines

- Make the main operation readable in execution order.
  Keep orchestration focused on domain steps such as reading a manifest, validating declarations, and resolving files.
  Keep the schema details and indexed error construction inside the step that owns them.
- Use names that identify domain values and their validation state, such as `sourceFiles`, `manifest`, and `declarations`.
  Introduce intermediate values when nesting forces readers to unpack several meaningful operations from the inside out.
  Do not create a temporary variable for every obvious expression.
- Extract a helper when it centralizes a repeated invariant or lets a reader skip meaningful implementation details.
  Give every named helper a concise contract describing its result, ordering, mutation, or failure behavior where relevant.
  Avoid pass-through wrappers whose names and interfaces communicate no more than the expression they wrap.
- Keep related helpers together in a module with one clear role.
  Export only the operations other modules need, and keep implementation helpers private.
  A useful internal module export does not automatically belong in a package or subsystem's public interface.
- Carry diagnostic context with validated data when later steps need to report the original source of an error.
  Preserve distinctions such as source-relative paths versus manifest field locations, declaration order versus sorted output, and absent configuration versus invalid configuration.
- Preserve behavior during extraction, including error precedence, duplicate handling, ordering, empty input, and mutation guarantees.
  Make intentional behavior changes explicit and verify them separately.
- Test through the interface callers use.
  Keep tests valid when private helpers are renamed, combined, or split.
  Avoid exporting helpers solely for tests or adding a matching test suite for every extracted function.
- Do not use function length, helper count, or the presence of a loop as sufficient evidence of a violation.
  Identify the mixed responsibilities, repeated invariant, or obscured processing step that makes the code harder to understand or change.

### Verification

Read the main operation without opening its helpers.
Its domain steps and ordering should be understandable from their names and contracts.
Then inspect each helper: its implementation should match that contract and concentrate the relevant details in one place.

When refactoring, run behavior tests covering valid input, absent and malformed configuration, precise error locations, duplicates, ordering, and missing referenced files as applicable.
The tests should verify observable results rather than the number or names of private helpers.
