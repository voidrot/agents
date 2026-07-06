---
name: go-naming
description: Choose and review Go package, identifier, receiver, interface, constructor, error, enum, acronym, and test names.
license: MIT
compatibility: Go projects using standard Go naming conventions.
metadata:
  owner: voidrot
---

# Go Naming

Use this skill when identifier names are part of the work. Go names should be short, clear at the call site, and consistent with visibility rules.

## Workflow

1. Identify the call site first; Go code is read with the package name included.
2. Remove stutter between package, type, and function names.
3. Apply visibility deliberately: exported names use UpperCamelCase; unexported names use lowerCamelCase.
4. Keep local names shorter when scope is tiny and more descriptive as scope widens.
5. Check acronyms, errors, constructors, enum zero values, and test names against the conventions below.
6. Use `go-code-style` when the issue is readability beyond naming.

## Quick Reference

| Element | Convention | Example |
| --- | --- | --- |
| Package | lowercase, short, usually singular | `auth`, `json`, `user` |
| File | lowercase; underscores are fine | `user_handler.go` |
| Exported identifier | UpperCamelCase | `HTTPClient`, `ReadAll` |
| Unexported identifier | lowerCamelCase | `parseToken` |
| Interface | behavior, often `-er` | `Reader`, `Validator` |
| Receiver | 1-2 letter type hint | `func (s *Server)` |
| Constructor | `New` for primary type, `NewType` when multiple types are created | `ring.New`, `http.NewRequest` |
| Sentinel error | `Err` prefix | `ErrNotFound` |
| Error type | `Error` suffix | `PathError` |
| Error string | lowercase, no punctuation | `"invalid id"` |
| Acronym | all caps or all lower | `HTTPServer`, `xmlParser` |
| Enum zero value | explicit unknown/invalid | `StatusUnknown` |
| Test | `Test` + subject; lowercase subtest names | `TestParseToken`, `"empty input"` |

## Constraints

- Avoid `util`, `helper`, `common`, and other package names that hide the domain.
- Avoid stutter such as `user.NewUser()` when callers can read `user.New()`.
- Do not use ALL_CAPS for constants; casing controls visibility, not emphasis.
- Do not use `Get` prefixes for ordinary getters; keep `Is`/`Has`/`Can` for boolean predicates.

## References

- For packages, files, and import aliases, read `references/packages-files.md`.
- For variables, booleans, receivers, and acronyms, read `references/identifiers.md`.
- For functions, methods, constructors, and options, read `references/functions-methods.md`.
- For types, constants, enums, and errors, read `references/types-errors.md`.
- For test naming conventions, read `references/testing.md`.
