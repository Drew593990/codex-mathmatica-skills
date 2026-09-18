# Changelog

## v0.3.0 — 2026-09-19

### Mathematical workflow

- Replace mandatory `First` formatting with justified candidate selection, retaining branches, parameter domains and unresolved cases.
- Separate execution assertions, mathematical evidence and requested delivery scope. Preserve raw proved/refuted/unresolved results; `TrueQ` False is not automatically a refutation.
- Distinguish conditional solutions, local/global optimality, Nash and SPE, including boundaries, degeneracy, unattained suprema, unilateral deviations and continuation quantifiers.
- Construct residuals before substitution and distinguish identities, solution-set equivalence and one-way implications.
- Keep numerical work conditional on task requirements; preserve full result/condition tables, source notation, stepwise derivation and rendered-report acceptance.

### Validators and example

- Reject empty/malformed checks, missing runtimes, early `Exit[0]`, missing completion markers and native-exit mismatches.
- Add advisory style checking by default, opt-in `--strict-style`, explicit `--no-runtime`, `--timeout` and `--work-dir`.
- Support non-ASCII target filenames through an ASCII wrapper path expression on Windows.
- Add the version-1 report contract and its regression tests; optional proof metadata does not replace formula status and is not mathematically authenticated.
- Label the bundled example as conditional stationary-point derivation. Preserve its original economic equations and existing public transformation assertion, with justified algebraic selection guards.
- Include Python protocol/report/integration tests and eleven exact Wolfram semantic regressions.

### Compatibility

- Keep the two skill names, existing validator entry points, original positional argument, `--wolfram`, `--no-runtime`, and `checks` row format.
- Intentional behavior changes: default validation now fails when runtime evidence is absent; style keywords are advisory unless strict mode is selected.
- Keep public paths and language configurable. No workstation configuration, personal session logs or local reader dependency is included.
- Preserve all prior releases and tags, including v0.2.3. Source history is extended rather than rewritten.

## Earlier releases

- [v0.2.3](https://github.com/Drew593990/codex-mathmatica-skills/releases/tag/v0.2.3): public documentation and example transformation check.
- [v0.2.2](https://github.com/Drew593990/codex-mathmatica-skills/releases/tag/v0.2.2): cross-platform installation, runtime and language guidance.
- [v0.2.1](https://github.com/Drew593990/codex-mathmatica-skills/releases/tag/v0.2.1): generalized runtime paths.
- [v0.2.0](https://github.com/Drew593990/codex-mathmatica-skills/releases/tag/v0.2.0): formula-transformation checks.
- [v0.1.0](https://github.com/Drew593990/codex-mathmatica-skills/releases/tag/v0.1.0): previous stable baseline.
