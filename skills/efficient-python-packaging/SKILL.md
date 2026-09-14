---
name: efficient-python-packaging
description: "Configure, change, review, and validate Python distribution packaging: pyproject build configuration, distribution metadata and versions, dependency boundaries, wheels, sdists, package data, entry points, and clean-install release checks. Use for installable Python package or CLI artifacts, not generic Python implementation, dependency selection, publishing accounts, or tooling migrations."
---

# Efficient Python Packaging

Use this skill when a Python project must produce or change an installable distribution. Preserve the repository's selected build backend, resolver, layout, and release process. Do not introduce a package manager, build backend, dependency, or project-wide tooling migration as part of packaging work.

Use `efficient-python` for Python implementation and package-layout behavior, `efficient-testing` for focused behavioral coverage, and `git-commit` only when preparing an authorized commit.

## Workflow

1. **Establish the distribution contract.** Read `pyproject.toml`, backend-specific configuration, repository instructions, package layout, version source, and existing build or release commands. Identify the distribution name versus import-package name, supported Python versions, public modules, runtime dependencies, optional features, package data, entry points, and intended artifacts. Inspect current consumers or tests before changing a published name, version source, import path, command name, extra, or dependency marker.
   - Treat the checked-in configuration and existing backend documentation in the repository as authoritative. Do not infer backend options from another backend or add compatibility configuration that the selected backend does not consume.
   - Keep build requirements limited to what the build backend needs to create the artifact. Keep runtime requirements limited to imports or runtime integrations needed by every installation. Put genuinely optional capabilities in the project's existing optional-dependency mechanism; do not put development, test, lint, or release tools in runtime dependencies.

2. **Make the smallest metadata and version change.** Keep required metadata truthful and synchronized with the files it references: name, version or dynamic version source, summary, Python requirement, licensing and author fields where the project uses them, classifiers, URLs, and readme content type. Use one established version source. If a version is dynamic, verify the backend can obtain it from a source included in the sdist; do not duplicate a static version merely to satisfy a tool.
   - Declare version bounds and environment markers only when the supported compatibility contract requires them. Do not select new dependencies or relax/tighten constraints without a concrete compatibility reason.
   - Update generated lock state only through the repository's established resolver workflow and only when a declared dependency change requires it. Never hand-edit generated resolution state.

3. **Configure inclusion deliberately.** Verify package discovery includes intended import packages and excludes tests, examples, build output, and incidental directories. Prefer the repository's current layout; do not move to a source layout solely for packaging work.
   - Include non-Python files only when installed code reads them at runtime. Configure them explicitly in the selected backend, then verify their paths and contents from the built wheel and sdist. Do not rely on a file being present in the checkout.
   - Add an entry point only for a requested supported command. Point it at a stable callable with a clear exit/error contract, preserve existing command names, and exercise the installed command.
   - Use a namespace package only when separate distributions are intentionally designed to share the same import namespace. Confirm discovery and installation behavior for each participating distribution; otherwise use a regular package and avoid namespace discovery settings.

4. **Build from a clean source state.** Remove or isolate prior distribution output using the repository's safe build procedure. Build both the wheel and sdist with the configured backend/frontend; do not substitute a new build tool. Record the exact command and Python environment. Treat build warnings about missing files, invalid metadata, or unexpected discovery as failures to investigate rather than noise.
   - Inspect artifact filenames and archive contents. Confirm the wheel contains the intended packages, package data, and metadata, while the sdist contains all source, metadata inputs, and version inputs needed to rebuild. Reject stale artifacts, local paths, secrets, tests accidentally shipped as library content, or expected runtime data missing from either artifact.

5. **Validate artifacts in disposable environments.** A checkout import, editable install, or test run against source does not validate a distribution. Create a fresh temporary environment outside the repository and install the built wheel from its artifact path. Run an import and the smallest public smoke path, including each changed entry point and runtime data lookup. Ensure the command runs with a working directory outside the checkout so source-tree imports cannot mask omissions.
   - Separately unpack the sdist into a fresh temporary directory, build it there with the established build path, and clean-install the resulting artifact into another disposable environment. Run the same relevant smoke path. This proves the sdist has sufficient build inputs rather than merely that its archive exists.
   - Resolve dependencies only through the project's normal policy. Do not use credentials, a production registry, or undeclared local source paths to make validation pass. If offline validation is not possible because required artifacts are unavailable, report it as blocked rather than silently using a different source.

6. **Run proportionate release-safe checks.** Run configured metadata, build, lint, type, test, and packaging checks that cover the changed boundary. Use `efficient-testing` to choose focused tests for changed import behavior, entry points, resources, or optional-dependency paths. Expand validation when shared build configuration, metadata, dependency declarations, or package discovery changed.
   - Compare installed-artifact behavior with the intended supported Python versions where the repository provides a supported matrix. Do not claim cross-version compatibility from a single interpreter.
   - Before a release handoff, confirm the source tree is clean apart from intended changes, artifact versions and filenames match the requested release, and no untracked distribution output or credentials are included. This skill does not publish artifacts or change publishing credentials, registry accounts, or release permissions.

## Failure handling

| Signal | Investigate first | Do not |
| --- | --- | --- |
| Import succeeds only in the checkout | Installed wheel from a disposable environment, package discovery, and source-path leakage | Modify `sys.path` or accept editable-install evidence |
| Data file missing after install | Wheel and sdist contents plus backend inclusion rules | Read files from a relative checkout path |
| sdist cannot build | Files and dynamic-version inputs included in the sdist | Ship a prebuilt wheel in place of fixing the sdist |
| Entry command fails | Installed entry-point metadata and target callable | Test only the callable from source |
| Unexpected dependency in artifact | Build/runtime/optional declaration boundary and markers | Add all development tools to runtime dependencies |
| Namespace import collision | Participating distribution discovery and clean-install order | Enable namespace discovery for an ordinary package |

## Completion evidence

Report the distribution contract changed or preserved; metadata/version and dependency-boundary decisions; package-data, entry-point, or namespace decision; wheel and sdist build commands and results; disposable clean-install commands and smoke results for both artifact paths; focused tests and configured checks run; checks skipped or blocked; and remaining compatibility or release risks. Do not claim release readiness when an artifact was not built and cleanly exercised outside the checkout.
