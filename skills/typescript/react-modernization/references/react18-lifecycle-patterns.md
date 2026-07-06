# React 18 Lifecycle Patterns

Migrated from `skills/.to-sort/react18-lifecycle-patterns/SKILL.md` into `skills/typescript/react-modernization`.

# React 18 Lifecycle Patterns

Reference for migrating the three unsafe class component lifecycle methods to React 18.3.1 compliant patterns.

## Quick Decision Guide

Before migrating any lifecycle method, identify the **semantic category** of what the method does. Wrong category = wrong migration. The table below routes you to the correct reference file.

### componentWillMount - what does it do?

| What it does | Correct migration | Reference |
|---|---|---|
| Sets initial state (`this.setState(...)`) | Move to `constructor` | [→ componentWillMount.md](react18-lifecycle-patterns-componentWillMount.md#case-a) |
| Runs a side effect (fetch, subscription, DOM) | Move to `componentDidMount` | [→ componentWillMount.md](react18-lifecycle-patterns-componentWillMount.md#case-b) |
| Derives initial state from props | Move to `constructor` with props | [→ componentWillMount.md](react18-lifecycle-patterns-componentWillMount.md#case-c) |

### componentWillReceiveProps - what does it do?

| What it does | Correct migration | Reference |
|---|---|---|
| Async side effect triggered by prop change (fetch, cancel) | `componentDidUpdate` | [→ componentWillReceiveProps.md](react18-lifecycle-patterns-componentWillReceiveProps.md#case-a) |
| Pure state derivation from new props (no side effects) | `getDerivedStateFromProps` | [→ componentWillReceiveProps.md](react18-lifecycle-patterns-componentWillReceiveProps.md#case-b) |

### componentWillUpdate - what does it do?

| What it does | Correct migration | Reference |
|---|---|---|
| Reads the DOM before update (scroll, size, position) | `getSnapshotBeforeUpdate` | [→ componentWillUpdate.md](react18-lifecycle-patterns-componentWillUpdate.md#case-a) |
| Cancels requests / runs effects before update | `componentDidUpdate` with prev comparison | [→ componentWillUpdate.md](react18-lifecycle-patterns-componentWillUpdate.md#case-b) |

---

## The UNSAFE_ Prefix Rule

**Never use `UNSAFE_componentWillMount`, `UNSAFE_componentWillReceiveProps`, or `UNSAFE_componentWillUpdate` as a permanent fix.**

Prefixing suppresses the React 18.3.1 warning but does NOT:
- Fix concurrent mode safety issues
- Prepare the codebase for React 19 (where these are removed, with or without the prefix)
- Fix the underlying semantic problem the migration is meant to address

The UNSAFE_ prefix is only appropriate as a temporary hold while scheduling the real migration sprint. Mark any UNSAFE_ prefix additions with:
```jsx
// TODO: React 19 will remove this. Migrate before React 19 upgrade.
// UNSAFE_ prefix added temporarily - replace with componentDidMount / getDerivedStateFromProps / etc.
```

---

## Reference Files

Read the full reference file for the lifecycle method you are migrating:

- **`references/react18-lifecycle-patterns-componentWillMount.md`** - 3 cases with full before/after code
- **`references/react18-lifecycle-patterns-componentWillReceiveProps.md`** - getDerivedStateFromProps trap warnings, full examples
- **`references/react18-lifecycle-patterns-componentWillUpdate.md`** - getSnapshotBeforeUpdate + componentDidUpdate pairing

Read the relevant file before writing any migration code.
