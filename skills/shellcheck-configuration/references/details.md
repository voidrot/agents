# shellcheck-configuration — detailed patterns and worked examples

## ShellCheck Fundamentals

### What is ShellCheck?

ShellCheck is a static analysis tool that analyzes shell scripts and detects problematic patterns. It supports:

- Bash, sh, dash, ksh, and other POSIX shells
- Over 100 different warnings and errors
- Configuration for target shell and flags
- Integration with editors and CI/CD systems

### Installation

```bash
# macOS with Homebrew
brew install shellcheck

# Ubuntu/Debian
apt-get install shellcheck

# From source
git clone https://github.com/koalaman/shellcheck.git
cd shellcheck
make build
make install

# Verify installation
shellcheck --version
```

## Configuration Files

### .shellcheckrc (Project Level)

Create `.shellcheckrc` in your project root:

```
# Specify target shell
shell=bash

# Enable optional checks
enable=avoid-nullary-conditions
enable=require-variable-braces

# Disable specific warnings
disable=SC1091
disable=SC2086
```

### Passing Options in Scripts and CI

ShellCheck does not define `SHELLCHECK_SHELL`, `SHELLCHECK_STRICT`, or
`SHELLCHECK_CONFIG` environment variables. Pass these settings as command-line
options instead:

```bash
shellcheck --shell=bash --enable=all --rcfile="$HOME/.shellcheckrc" script.sh
```

## Common ShellCheck Error Codes

### SC1000-1099: Syntax and Parser Diagnostics

Diagnostics in this range cover shell syntax and parser issues. Use the exact
code and message reported by ShellCheck when investigating a parser failure;
these diagnostics can depend on the selected shell dialect and shebang.

### SC2000-2099: Shell Issues

```bash
# SC2009: Consider using pgrep or pidof instead of grep|grep
ps aux | grep -v grep | grep myprocess  # Use pgrep instead

# SC2012: Use `ls` only for viewing. Use `find` for reliable output
for file in $(ls -la)  # Better: use find or globbing

# SC2015: Avoid using && and || instead of if-then-else
[[ -f "$file" ]] && echo "found" || echo "not found"  # Less clear

# SC2016: Expressions don't expand in single quotes
echo '$VAR'  # Literal $VAR, not variable expansion

```

### SC2100-2199: Quoting Issues

```bash
# SC2086: Double quote to prevent word splitting and globbing
for i in $list; do  # BAD: unquoted scalar expansion
    echo "$i"
done

# GOOD: use an array when iterating over multiple values
for i in "${list[@]}"; do
    echo "$i"
done

# SC2115: Guard a directory variable before recursive removal
rm -rf "$dir"/*  # Warns if an empty $dir could expand to /*
rm -rf -- "${dir:?}"/*

# SC2181: Check exit code directly with `if`, not indirectly in a list
some_command
if [ $? -eq 0 ]; then  # Better: if some_command; then

# SC2206: Quote to prevent word splitting or split explicitly
array=( $items )  # BAD: unquoted array expansion
read -r -a array <<< "$items"
```

### SC3000-3999: POSIX Compliance Issues

```bash
# SC3010: In POSIX sh, `[[ ]]` is undefined
if [[ $var == "value" ]]; then  # Use [ ] or test in POSIX sh
    do_something
fi

# SC3043: In POSIX sh, 'local' is undefined
function my_func() {
    local var=value  # Not POSIX in some shells
}
```

## Practical Configuration Examples

### Minimal Configuration (Strict POSIX)

```bash
#!/bin/bash
# Configure for maximum portability

shellcheck \
  --shell=sh \
  --external-sources \
  --check-sourced \
  script.sh
```

### Development Configuration (Bash with Relaxed Rules)

```bash
#!/bin/bash
# Configure for Bash development

shellcheck \
  --shell=bash \
  --exclude=SC1091,SC2119 \
  --enable=all \
  script.sh
```

### CI/CD Integration Configuration

```bash
#!/bin/bash
set -Eeuo pipefail

# Analyze all shell scripts and fail on issues
find . -type f -name "*.sh" | while read -r script; do
    echo "Checking: $script"
    shellcheck \
        --shell=bash \
        --format=gcc \
        --exclude=SC1091 \
        "$script" || exit 1
done
```

### .shellcheckrc for Project

```
# Shell dialect to analyze against
shell=bash

# Enable optional checks
enable=avoid-nullary-conditions,require-variable-braces,check-unassigned-uppercase

# Disable specific warnings
# SC1091: Not following sourced files (many false positives)
disable=SC1091

# SC2119: Use `function_name "$@"` if the function's `$1` should mean the script's `$1`
disable=SC2119

# External files to source for context
external-sources=true
```

## Integration Patterns

### Pre-commit Hook Configuration

```bash
#!/bin/bash
# .git/hooks/pre-commit
set -e

# Find all shell scripts changed in this commit
git diff --cached --name-only | grep '\.sh$' | while read -r script; do
    echo "Linting: $script"

    if ! shellcheck "$script"; then
        echo "ShellCheck failed on $script"
        exit 1
    fi
done
```

### GitHub Actions Workflow

```yaml
name: ShellCheck

on: [push, pull_request]

jobs:
  shellcheck:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Run ShellCheck
        run: |
          sudo apt-get install shellcheck
          find . -type f -name "*.sh" -exec shellcheck {} \;
```

### GitLab CI Pipeline

```yaml
shellcheck:
  stage: lint
  image: koalaman/shellcheck-alpine
  script:
    - find . -type f -name "*.sh" -exec shellcheck {} \;
  allow_failure: false
```

## Handling ShellCheck Violations

### Suppressing Specific Warnings

```bash
#!/bin/bash

# Disable warning for entire line
# shellcheck disable=SC2086
for file in $(ls -la); do
    echo "$file"
done

# Disable for entire script
# shellcheck disable=SC1091,SC2119

# Disable multiple warnings (format varies)
command_that_fails() {
    # shellcheck disable=SC2015
    [ -f "$1" ] && echo "found" || echo "not found"
}

# Disable specific check for source directive
# shellcheck source=./helper.sh
source helper.sh
```

### Common Violations and Fixes

#### SC2086: Double quote to prevent word splitting

```bash
# Problem
for i in $list; do done

# Solution
for i in $list; do done  # If $list is already quoted, or
for i in "${list[@]}"; do done  # If list is an array
```

#### SC2181: Check exit code directly

```bash
# Problem
some_command
if [ $? -eq 0 ]; then
    echo "success"
fi

# Solution
if some_command; then
    echo "success"
fi
```

#### SC2015: Use if-then instead of && ||

```bash
# Problem
[ -f "$file" ] && echo "exists" || echo "not found"

# Solution - clearer intent
if [ -f "$file" ]; then
    echo "exists"
else
    echo "not found"
fi
```

#### SC2016: Expressions don't expand in single quotes

```bash
# Problem
echo 'Variable value: $VAR'

# Solution
echo "Variable value: $VAR"
```

#### SC2009: Use pgrep instead of grep

```bash
# Problem
ps aux | grep -v grep | grep myprocess

# Solution
pgrep -f myprocess
```

## Performance Optimization

### Checking Multiple Files

```bash
#!/bin/bash

# Sequential checking
for script in *.sh; do
    shellcheck "$script"
done

# Parallel checking (faster)
find . -name "*.sh" -print0 | \
    xargs -0 -P 4 -n 1 shellcheck
```

### Caching Results

```bash
#!/bin/bash

CACHE_DIR=".shellcheck_cache"
mkdir -p "$CACHE_DIR"

check_script() {
    local script="$1"
    local hash
    local cache_file

    hash=$(sha256sum "$script" | cut -d' ' -f1)
    cache_file="$CACHE_DIR/$hash"

    if [[ ! -f "$cache_file" ]]; then
        if shellcheck "$script" > "$cache_file" 2>&1; then
            touch "$cache_file.ok"
        else
            return 1
        fi
    fi

    [[ -f "$cache_file.ok" ]]
}

find . -name "*.sh" | while read -r script; do
    check_script "$script" || exit 1
done
```

## Output Formats

### Default Format

```bash
shellcheck script.sh

# Output:
# script.sh:1:3: warning: foo is referenced but not assigned. [SC2154]
```

### GCC Format (for CI/CD)

```bash
shellcheck --format=gcc script.sh

# Output:
# script.sh:1:3: warning: foo is referenced but not assigned.
```

### JSON Format (for parsing)

```bash
shellcheck --format=json script.sh

# Output:
# [{"file": "script.sh", "line": 1, "column": 3, "level": "warning", "code": 2154, "message": "..."}]
```

### Quiet Format

```bash
shellcheck --format=quiet script.sh

# Returns non-zero if issues found, no output otherwise
```
