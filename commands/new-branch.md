---
description: Create and optionally switch to a new Git branch, with safe handling for uncommitted work.
model: openai/gpt-5.4-mini
---

You are helping the user create a new Git branch.

Arguments supplied by the user:

```text
$ARGUMENTS
```

## Load relevant skills

Before acting, load Git-related skills when they apply and would improve correctness or safety, especially:

- @git-flow-branch-creator for branch type/name selection and Git Flow conventions.
- @git-workflow for repository branch policy or naming conventions.
- @git-advanced-workflows for unusual repository states, worktrees, rebases, detached HEAD, or conflict recovery.

## Supported arguments

- `--switch`: create the branch and switch to it. If there is uncommitted work in the current worktree, carry that work onto the new branch by switching normally with Git.
- Optional branch name or purpose text: everything that is not a recognized flag may be either the exact branch name or details from which to infer one.

If `--switch` is not supplied, default to `--switch` unless the user's wording clearly asks to stay on the current branch.

## Branch name handling

1. Parse recognized flags first.
2. Treat a remaining argument that already looks like a branch name as the branch name.
3. If the remaining argument is descriptive purpose text, infer a concise branch name from it.
4. Prefer repository conventions if discoverable from existing branches or project guidance.
5. Sanitize inferred names for Git:
   - lowercase words;
   - hyphen separators;
   - no spaces;
   - no `..`, `@{`, leading slash, trailing slash, or trailing dot;
   - avoid shell metacharacters.
6. If no branch name is supplied and no meaningful purpose/details are available, ask the user one concise question: what branch name they want, or what the branch is for.

## Safety checks

Before creating the branch:

1. Check the current Git state with non-interactive commands.
2. Detect whether the current directory is a Git repository.
3. Identify the current branch or detached-HEAD state.
4. Check for uncommitted work and untracked files.
5. Check whether the target branch already exists locally or remotely.

Do not overwrite, delete, stash, reset, or discard user work unless the user explicitly asked for that. If the requested branch name already exists, stop and report the conflict with the safest next options.

## Execution

- For `--switch`, create and switch in one safe Git operation, normally:

  ```bash
  git switch -c "<branch-name>"
  ```

- For `--keep`, create the branch without switching, normally:

  ```bash
  git branch "<branch-name>"
  ```

Use shell quoting for the branch name. Prefer `git switch` over legacy `git checkout` unless the environment requires a fallback.

## Final response

Keep the final response terse. Include:

- created branch name;
- whether the session switched to it or kept the previous branch;
- how uncommitted work was handled;
- any relevant warning or next step, only if needed.
