# Conflict resolution playbook

## State discovery

```bash
git status
git diff --name-only --diff-filter=U
git branch --show-current
git log --oneline --decorate -n 20
```

Check whether `.git/MERGE_HEAD`, `.git/rebase-merge`, `.git/rebase-apply`, `CHERRY_PICK_HEAD`, or `REVERT_HEAD` exists when the operation type is unclear.

## Conflict marker anatomy

```text
<<<<<<< HEAD
current side
=======
incoming side
>>>>>>> feature-branch
```

During rebase, remember that "ours" and "theirs" can feel inverted relative to normal branch language. Confirm the operation before choosing sides.

## Resolution patterns

### Preserve both compatible changes

Use when both sides added independent validation, branches, tests, imports, or fields.

1. Combine the code intentionally.
2. Remove duplicated imports or declarations.
3. Run tests that cover both behaviors.

### Pick one side with justification

Use when one side deletes or replaces a concept and the other edits the old concept.

Document why the kept side matches the merge goal:

- target branch intentionally removed the feature;
- incoming branch contains the newer API;
- one side is generated/stale;
- one side conflicts with a migration or product decision.

### Regenerate generated files

For lockfiles, generated clients, snapshots, compiled assets, or schema output:

1. Resolve source files first.
2. Re-run the generating command.
3. Stage generated output.
4. Run verification that uses the regenerated artifact.

### Rename/delete conflicts

Decide whether the file should exist at the new path, old path, or be removed. Move edits from the deleted/old path into the kept path when both intents matter.

### Binary conflicts

Do not hand-edit. Choose the correct artifact, regenerate from source, or ask for the authoritative binary if neither side can be validated.

## Useful commands

```bash
# List unresolved files
git diff --name-only --diff-filter=U

# Inspect each side of a conflicted file
git show :1:path/to/file   # common ancestor
git show :2:path/to/file   # ours
git show :3:path/to/file   # theirs

# Accept one side only when justified
git checkout --ours path/to/file
git checkout --theirs path/to/file

# Stage resolved files
git add path/to/file

# Continue operation
git rebase --continue
git cherry-pick --continue
git revert --continue
git commit --no-edit
```

Use non-interactive commit messages or `--no-edit` where appropriate in automated environments.

## Verification checklist

- [ ] `git diff --name-only --diff-filter=U` returns no files.
- [ ] Conflict markers are absent from resolved text files.
- [ ] The resolution preserves or explicitly rejects each side's intent.
- [ ] Generated files/lockfiles were regenerated when needed.
- [ ] Relevant tests/typechecks/format checks pass or failures are documented.
- [ ] Merge/rebase/cherry-pick/revert state is completed or clearly paused with next command.
