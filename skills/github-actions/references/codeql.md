# CodeQL reference

Read this only when the request explicitly covers CodeQL setup or configuration, a CodeQL SARIF result, or a CodeQL build/analysis failure. It supplements the workflow and security references; do not repeat their trigger, permission, or action-ref decisions.

## Establish the analysis boundary

1. Consult the current official [CodeQL code scanning documentation](https://docs.github.com/en/code-security/code-scanning/introduction-to-code-scanning/about-code-scanning-with-codeql), [advanced setup guidance](https://docs.github.com/en/code-security/code-scanning/setting-up-code-scanning/configuring-advanced-setup-for-code-scanning), and [CodeQL action README/releases](https://github.com/github/codeql-action) before selecting syntax, supported languages, build modes, limits, or compatibility. Check the documented action/CLI version and inputs against the repository's existing configuration; do not infer either from old examples or prescribe a version here.
2. Identify whether default setup, advanced setup, or a locally run CodeQL CLI currently owns each requested language. Do not introduce a second owner for the same analysis without an explicit, documented migration or separation.
3. Inventory the languages, source roots, generated/vendor directories, build systems, and intended components. Select only documented language identifiers and one supported build mode per analysis unit. Choose no-build analysis only when its documented coverage is appropriate; otherwise use documented automatic or explicit build handling. For compiled code, the build must run after database initialization and compile the intended production targets, not merely restore dependencies, lint, or run a partial test target.

## Configure and verify deliberately

- Keep CodeQL-specific initialization, build, analysis, and result handling within the scan job's documented ordering. Do not fold unrelated CI, deployment, or security-policy changes into the scan request.
- In a monorepo, make each analysis unit's source scope and build command explicit. Give independently uploaded result sets stable, distinct categories as documented, and verify that every intended component and language is built or otherwise extracted. Do not use path exclusions to conceal an unverified build gap.
- Treat SARIF as analysis output, not a generic artifact format: retain the analysis identity/category and the run ref/commit association required by the current upload documentation. Before upload or diagnosis, check the generated file's format, size and result limits, and any validation errors against the current [SARIF support documentation](https://docs.github.com/en/code-security/code-scanning/integrating-with-code-scanning/sarif-support-for-code-scanning). Do not edit findings, fingerprints, locations, or provenance merely to make an upload succeed.

## Diagnose with evidence

Start with the first failing CodeQL step and record the workflow revision, event/ref/SHA, language, build mode, source scope, runner OS, and exact build or analysis command. Then inspect the relevant initialization, extraction, build, and SARIF/upload messages to distinguish unsupported configuration, a failed/incomplete build, missing source coverage, malformed or oversized SARIF, and upload authorization or association failures. Reproduce the project build at the same revision where safely possible; report which targets compiled and which source roots were extracted. Use current official troubleshooting guidance rather than changing modes, exclusions, categories, or access as a blind workaround.

## Sources

Official GitHub documentation and the `github/codeql-action` repository are the compatibility sources for this reference. Recheck them live for every CodeQL configuration or failure because supported languages, build modes, action inputs, SARIF limits, and release compatibility change.
