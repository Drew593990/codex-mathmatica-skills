# Codex Mathmatica Skills

Codex Mathmatica Skills is a small skill set for using Wolfram/Mathematica as a serious symbolic engine inside AI-assisted mathematical and economic-theory work. The core purpose is not merely to generate plausible formulas, but to make derivations auditable: start from model primitives, run Mathematica checks, keep intermediate objects visible, and reject results that do not pass explicit verification.

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
- strict Boolean check tables and hard-fail guards;
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
- add strict Boolean checks for every major claim.

The distinctive rule in this skill is the formula-transformation check. When a raw derivative or constraint is rewritten into an economic target form, such as a markup equation, best-response condition, threshold boundary, or welfare ranking, the agent must construct both a raw residual and a target residual, record any nonzero multiplier assumptions, and verify equivalence with Mathematica. `FullSimplify` is used as a verifier, not as a substitute for economic interpretation.

## Typical Workflow

1. Identify players, timing, variables, assumptions, constraints, objectives, and equilibrium concept.
2. Translate the primitive model into Wolfram Language with source notation preserved.
3. Run small Mathematica derivation steps and keep important outputs visible.
4. Derive FOCs, SOC/Hessian conditions, feasibility regions, and candidate solutions.
5. Convert raw expressions into interpretable economic forms and verify residual equivalence.
6. Build a `checks` table where every result is exactly `True` or `False`.
7. Run the generated `.wl` with a local Wolfram executable and inspect stdout plus exported checks.
8. Use reports, CSVs, plots, or summary grids only after the symbolic and runtime checks pass.

## Included Files

- Style example: [`skills/paper-proposition-mathematica/examples/mfn-rpm-nonash-competition-style.wl`](skills/paper-proposition-mathematica/examples/mfn-rpm-nonash-competition-style.wl)
- Validator: [`skills/paper-proposition-mathematica/scripts/validate_wl_derivation.py`](skills/paper-proposition-mathematica/scripts/validate_wl_derivation.py)
- Style guide: [`skills/paper-proposition-mathematica/references/mathematica-style-guide.md`](skills/paper-proposition-mathematica/references/mathematica-style-guide.md)

The bundled example demonstrates a runnable paper-proposition-style `.wl` derivation with regime objects, summary grids, Boolean checks, and a residual-equivalence check for a best-response transformation.

## Installation

Copy the desired skill folder into your Codex skills directory.

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
- Python 3.9 or newer for `scripts/validate_wl_derivation.py`. If Python is unavailable, skip the validator and rely on direct Wolfram runtime checks.

## Wolfram Runtime

These skills do not assume a fixed Wolfram executable path. Prefer a user-provided path, environment variable, command on `PATH`, or detected platform install location. Example:

```powershell
& '<path-to-wolfram>\wolfram.exe' -script '<absolute-path-to-script.wl>'
```

Use the local shell's syntax when substituting the discovered executable path.

## Verification

For full derivation tasks, completion should be supported by concrete evidence:

- the `.wl` script runs with exit code `0`;
- stdout contains the script's success marker, such as `ALL_CHECKS_TRUE`;
- exported check rows are strict Boolean `True` values;
- numeric benchmarks, if used, are derived from independent solving or primitive residual checks;
- plots or reports are generated only after the symbolic checks pass.

The validator script is useful as a secondary style/runtime check, but it is not a replacement for a direct Wolfram run.

## License

MIT License. See [LICENSE](LICENSE).
