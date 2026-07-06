# React 18 String Refs Migration

Migrated from `skills/.to-sort/react18-string-refs/SKILL.md` into `skills/typescript/react-modernization`.

# React 18 String Refs Migration

String refs (`ref="myInput"` + `this.refs.myInput`) were deprecated in React 16.3, warn in React 18.3.1, and are **removed in React 19**.

## Quick Pattern Map

| Pattern | Reference |
|---|---|
| Single ref on a DOM element | [→ patterns.md#single-ref](react18-string-refs-patterns.md#single-ref) |
| Multiple refs in one component | [→ patterns.md#multiple-refs](react18-string-refs-patterns.md#multiple-refs) |
| Refs in a list / dynamic refs | [→ patterns.md#list-refs](react18-string-refs-patterns.md#list-refs) |
| Callback refs (alternative approach) | [→ patterns.md#callback-refs](react18-string-refs-patterns.md#callback-refs) |
| Ref passed to a child component | [→ patterns.md#forwarded-refs](react18-string-refs-patterns.md#forwarded-refs) |

## Scan Command

```bash
# Find all string ref assignments in JSX
grep -rn 'ref="' src/ --include="*.js" --include="*.jsx" | grep -v "\.test\."

# Find all this.refs accessors
grep -rn "this\.refs\." src/ --include="*.js" --include="*.jsx" | grep -v "\.test\."
```

Both should be migrated together - find the `ref="name"` and the `this.refs.name` accesses for each component as a pair.

## The Migration Rule

Every string ref migrates to `React.createRef()`:

1. Add `refName = React.createRef();` as a class field (or in constructor)
2. Replace `ref="refName"` → `ref={this.refName}` in JSX
3. Replace `this.refs.refName` → `this.refName.current` everywhere

Read `references/react18-string-refs-patterns.md` for the full before/after for each case.
