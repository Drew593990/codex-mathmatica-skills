# Codex Mathmatica Skills

Codex Mathmatica Skills is a small skill set for using Wolfram/Mathematica as a serious symbolic engine inside AI-assisted mathematical and economic-theory work. The core purpose is not merely to generate plausible formulas, but to make derivations auditable: start from model primitives, run Mathematica checks, keep intermediate objects visible, and keep execution checks distinct from mathematical proof and report acceptance.

The repository provides two complementary skills:

- `mathmatica-user`: a general Wolfram Language modeling skill for symbolic mathematics, optimization, equilibrium solving, formula verification, and numeric simulation.
- `paper-proposition-mathematica`: a stricter economics-paper workflow skill for reproducing, checking, extending, and documenting theoretical propositions in a readable `.wl` derivation style.

The spelling `mathmatica-user` is intentional. It matches the original trigger name used by the workflow this repository was extracted from, and is preserved for compatibility with existing installations.

## Core Purpose

These skills are designed for tasks where an AI agent should use Mathematica as a verification partner rather than as a decorative code generator. They emphasize:

- primitive-first model construction;
- visible step-by-step symbolic derivation;
- Wolfram-native notation, including Greek symbols such as `\[Theta]`, `\[Alpha]`, and `\[Gamma]`;
- explicit FOC, SOC/Hessian, feasibility, threshold, and ranking checks;
- economically meaningful formula transformations verified through residual equivalence;
- nonempty, strictly Boolean technical check tables and hard-fail guards;
- raw mathematical evidence with proved/refuted/unresolved status and explicit proof scope;
- direct execution with a discovered local Wolfram runtime.

## Skill Overview

### `mathmatica-user`

Use `mathmatica-user` when a task needs Mathematica/Wolfram Language as the primary symbolic engine. It is designed for:

- translating mathematical and economic model primitives into Wolfram Language;
- deriving first-order conditions, second-order conditions, Hessians, feasible regions, equilibrium candidates, and comparative statics;
- verifying algebraic equivalence between alternative formula forms;
- running exact symbolic checks before numeric substitution;
- producing reproducible `.wl` scripts, CSV outputs, plots, and reports when appropriate;
- discovering and using a local Wolfram runtime rather than assuming a fixed executable path.

The skill is suitable for general modeling tasks beyond economics as long as the task benefits from symbolic derivation, formula verification, or reproducible Mathematica execution.

### `paper-proposition-mathematica`

Use `paper-proposition-mathematica` when the task is to reproduce or audit an economics paper proposition.

This skill is stricter because paper-style theoretical work has more ways to go wrong. It requires the agent to:

- start from the paper's primitive definitions rather than from final formulas;
- preserve source notation where possible, including Wolfram-native Greek symbols and direct primitives such as `F[\[Theta]]` and `f[\[Theta]]`;
- run Mathematica step by step while deriving, then assemble a readable `.wl` only after the derivation is clear;
- keep key intermediate objects visible, including FOCs, SOC/Hessian checks, solution lists, selected rules, threshold equations, feasible regions, regime associations, and summary grids;
- avoid unexplained shortcut symbols after model setup;
- compare symbolic results to primitive residual checks or independent numeric solving when benchmarks are needed;
- preserve raw mathematical evidence for required claims, and separately register strict Boolean technical assertions.

Candidate selection must be justified by the model and domain, not solver ordering. Local/global optimality, Nash and SPE require different evidence. Strict Hessian negativity is not necessary for every optimum, and numerical examples cannot replace symbolic proof.

The distinctive rule in this skill is the formula-transformation check. When a raw derivative or constraint is rewritten into an economic target form, such as a markup equation, best-response condition, threshold boundary, or welfare ranking, the agent must construct both a raw residual and a target residual, record any nonzero multiplier assumptions, and verify equivalence with Mathematica. `FullSimplify` is used as a verifier, not as a substitute for economic interpretation.

## Typical Workflow

1. Identify players, timing, variables, assumptions, constraints, objectives, and equilibrium concept.
2. Translate the primitive model into Wolfram Language with source notation preserved.
3. Run small Mathematica derivation steps and keep important outputs visible.
4. Derive FOCs, SOC/Hessian conditions, feasibility regions, and candidate solutions.
5. Construct residuals before substitution; distinguish algebraic identities, equivalent solution sets and one-way implications.
6. Preserve raw results and proof scope; build a nonempty technical `checks` table with valid named Boolean rows.
7. Run the generated `.wl` once through the runtime validator and inspect its completion evidence and exported checks.
8. Accept the requested mathematical result and report separately. A verified refutation can complete an audit; an unresolved required positive proof remains incomplete.

## Included Files

- Style example: [`skills/paper-proposition-mathematica/examples/mfn-rpm-nonash-competition-style.wl`](skills/paper-proposition-mathematica/examples/mfn-rpm-nonash-competition-style.wl)
- Validator: [`skills/paper-proposition-mathematica/scripts/validate_wl_derivation.py`](skills/paper-proposition-mathematica/scripts/validate_wl_derivation.py)
- Style guide: [`skills/paper-proposition-mathematica/references/mathematica-style-guide.md`](skills/paper-proposition-mathematica/references/mathematica-style-guide.md)
- Shared research requirements: [research-delivery-rules.md](skills/paper-proposition-mathematica/references/research-delivery-rules.md)
- Report acceptance and version-1 contract: [report-quality-gate.md](skills/paper-proposition-mathematica/references/report-quality-gate.md)
- Report checker: [validate_report_contract.py](skills/paper-proposition-mathematica/scripts/validate_report_contract.py)
- Exact semantic regressions: [verification_semantics.wl](skills/paper-proposition-mathematica/scripts/tests/verification_semantics.wl)

The bundled example demonstrates conditional algebraic stationary points, regime objects, summary grids and a FOC transformation check. Its ten registered checks do **not** establish nonnegative demand, global optimality or complete equilibrium over its original parameter domain. The original formulas and the negative-demand counterexample are retained to make this boundary testable.

## Installation

Copy the skill folders into the skills directory configured for your Codex installation. Install both together: `mathmatica-user` references shared resources in `paper-proposition-mathematica`. Back up existing folders before updating them.

PowerShell:

```powershell
Copy-Item -Recurse .\skills\mathmatica-user $env:CODEX_HOME\skills\
Copy-Item -Recurse .\skills\paper-proposition-mathematica $env:CODEX_HOME\skills\
```

Bash / Zsh:

```bash
cp -r ./skills/mathmatica-user "$CODEX_HOME/skills/"
cp -r ./skills/paper-proposition-mathematica "$CODEX_HOME/skills/"
```

If `CODEX_HOME` is not set, copy the folders into your local skills directory for the agent platform you use.

## Prerequisites

- A local Wolfram/Mathematica installation for running generated `.wl` scripts.
- Python 3.10 or newer for the bundled validators and tests; they use the standard library.
- If Python is unavailable, direct Wolfram execution requires equivalent nonempty check validation and completion evidence. Do not report Python validation as performed.

## Wolfram Runtime

These skills do not assume a fixed Wolfram executable path. Prefer a user-provided path, environment variable, command on `PATH`, or detected platform install location. Example:

```powershell
& '<path-to-wolfram>\wolfram.exe' -script '<absolute-path-to-script.wl>'
```

Use the local shell's syntax when substituting the discovered executable path.

## Verification

Run from the repository root, replacing the executable and paths with those in your environment:

```shell
python skills/paper-proposition-mathematica/scripts/validate_wl_derivation.py model.wl --wolfram "/path/to/wolfram" --work-dir "/path/to/task/runtime" --timeout 180
```

The wrapper actually executes the target. A second complete run is unnecessary when the wrapper has supplied the required evidence. It checks a nonempty list of exactly two-element rows, a nonblank string name in every row, strictly Boolean results, a unique completion marker for the current run and a matching native exit status. Normally completing target scripts must not call `Exit[0]`, because that prevents the wrapper from completing.

Style-token checks are advisory by default. `--strict-style` makes the heuristic style check blocking; it does not prove mathematics. `--no-runtime` explicitly performs only static inspection and prints `RUNTIME_VALIDATION_NOT_REQUESTED`. Missing Wolfram is an error in default mode, not a successful static fallback. Use `--work-dir` to respect task-specific temporary-file placement.

| Exit | Meaning |
|---|---|
| 0 | Registered runtime checks passed, or explicit static-only inspection completed; inspect the output mode |
| 2 | Invalid input, unreadable file or work-directory problem |
| 3 | Strict style check failed |
| 4 | Runtime unavailable or could not be launched |
| 5 | Target execution failed or the native process failed without a completion marker |
| 6 | Runtime timeout |
| 21 | Missing `checks` |
| 22 | Non-Boolean check results |
| 23 | False technical check |
| 24 | Empty or non-list `checks` |
| 25 | Malformed check row or label |
| 26 | Missing, duplicate, unknown or inconsistent completion evidence |

`RUNTIME_VALIDATION_OK` (and compatibility alias `VALIDATION_OK`) verifies the registered technical assertions only. The validator is neither a mathematical proof checker nor a security sandbox. Preserve unknown mathematical results and review the requested optimality/equilibrium claim separately. Report-contract success likewise does not authenticate mathematical truth, optional proof metadata or rendered layout.

## Regression tests

Run the Python suite:

```shell
python -m unittest discover -s skills/paper-proposition-mathematica/scripts -p "test_*.py" -v
```

Set `WL_VALIDATION_TEST_EXE` to the actual Wolfram executable to enable the six real-kernel integration test methods. Without it, those methods are explicitly skipped; do not report them as passed. `WL_VALIDATION_TEST_ROOT` and `REPORT_GATE_TEST_ROOT` optionally choose existing temporary-work directories; otherwise tests use the operating system's temporary directory.

Run the eleven exact mathematical cases with the same executable:

```shell
python skills/paper-proposition-mathematica/scripts/validate_wl_derivation.py skills/paper-proposition-mathematica/scripts/tests/verification_semantics.wl --wolfram "/path/to/wolfram" --work-dir "/path/to/task/runtime"
```

The small cases cover residual evaluation, equation equivalence, zero-factor cancellation, flat Hessians, boundary optima, nonattainment, vacuous implications, multiple roots, unresolved claims and simultaneous substitution. They do not establish autonomous correctness on arbitrary research tasks.

## Versions and rollback

The current release is **v0.3.0**; see [CHANGELOG.md](CHANGELOG.md). Previous releases and tags, including **v0.2.3**, remain available with their original source history. Updates add commits and new tags rather than replacing older release tags.

To inspect or install the prior version from an isolated checkout:

```shell
git clone --branch v0.2.3 https://github.com/Drew593990/codex-mathmatica-skills.git codex-mathmatica-skills-v0.2.3
```

Back up any customized installed skill folders before copying files from that checkout. Do not use a force push or delete old tags to roll back a local installation.

## License

MIT License. See [LICENSE](LICENSE).
