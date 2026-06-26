# Codex Mathmatica Skills

Codex skills for Wolfram/Mathematica-based mathematical modeling, symbolic derivation, economics paper proposition replication, and auditable equilibrium verification.

The repository contains two complementary skills:

- `mathmatica-user`: a general Wolfram Language modeling skill for symbolic mathematics, optimization, equilibrium solving, formula verification, and numeric simulation.
- `paper-proposition-mathematica`: a stricter economics-paper workflow skill for reproducing, checking, extending, and documenting theoretical propositions in a human-readable `.wl` derivation style.

The spelling `mathmatica-user` is intentional because it matches the original skill trigger used by this workflow.

## Skills

### `mathmatica-user`

Use `mathmatica-user` when a task needs Mathematica/Wolfram Language as the primary symbolic engine. It is designed for:

- translating mathematical and economic model primitives into Wolfram Language;
- deriving first-order conditions, second-order conditions, Hessians, feasible regions, equilibrium candidates, and comparative statics;
- verifying algebraic equivalence between alternative formula forms;
- running exact symbolic checks before numeric substitution;
- producing reproducible `.wl` scripts, CSV outputs, plots, and short reports when needed;
- discovering and using a local Wolfram runtime rather than assuming a fixed executable path.

The skill emphasizes reproducibility. Generated scripts should contain explicit assumptions, symbolic objects, strict Boolean checks, and hard-fail guards so that false or malformed checks do not silently pass.

### `paper-proposition-mathematica`

Use `paper-proposition-mathematica` when the task is to reproduce or audit an economics paper proposition.

It is stricter than the general skill. It requires:

- starting from the paper's primitive definitions rather than from final formulas;
- preserving source notation, including Wolfram-native Greek symbols such as `\[Theta]`, `\[Alpha]`, `\[Gamma]`, and direct distribution primitives such as `F[\[Theta]]` and `f[\[Theta]]`;
- running Mathematica step by step while deriving, then assembling a readable `.wl` script only after the derivation is clear;
- leaving key intermediate objects visible, including FOCs, SOC/Hessian checks, solution lists, selected rules, threshold equations, feasible regions, regime associations, and summary grids;
- avoiding unexplained shortcut symbols after model setup;
- checking every major result with strict Boolean verification rows;
- comparing symbolic results to independent numeric solving or primitive residual checks when numeric benchmarks are needed.

The skill also contains a specific pattern for economically meaningful formula transformations. At important steps, the agent must choose the target economic form, such as inverse-hazard markup, Lerner/unit-margin expressions, threshold boundaries, envelope conditions, or welfare rankings, then verify equivalence by constructing raw residuals and target residuals under explicit nonzero multiplier assumptions. `FullSimplify` is used as a verifier, not as a substitute for economic interpretation.

## Typical Workflow

1. Identify primitives, players, timing, decision variables, assumptions, constraints, and equilibrium concept.
2. Write a stepwise Mathematica derivation from the primitive model.
3. Keep visible intermediate outputs for the economically important steps.
4. Solve FOCs and check SOC/Hessian or feasible-region conditions.
5. Transform raw formulas into interpretable economic forms and verify equivalence.
6. Build a strict `checks` table where each result is exactly `True` or `False`.
7. Run the generated `.wl` through a local Wolfram executable and inspect exported outputs.
8. Use reports, CSVs, plots, or summary grids as presentation artifacts after verification.

## Included Files

- Style example: [`skills/paper-proposition-mathematica/examples/mfn-rpm-nonash-competition-style.wl`](skills/paper-proposition-mathematica/examples/mfn-rpm-nonash-competition-style.wl)
- Validator: [`skills/paper-proposition-mathematica/scripts/validate_wl_derivation.py`](skills/paper-proposition-mathematica/scripts/validate_wl_derivation.py)
- Style guide: [`skills/paper-proposition-mathematica/references/mathematica-style-guide.md`](skills/paper-proposition-mathematica/references/mathematica-style-guide.md)

## Installation

Copy the desired skill folder into your Codex skills directory:

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

If `CODEX_HOME` is not set, copy the folders into your local Codex skills directory manually.

## Prerequisites

- A local Wolfram/Mathematica installation for running generated `.wl` scripts.
- Python 3.9 or newer for `scripts/validate_wl_derivation.py`. If Python is unavailable, skip the validator and use direct Wolfram runtime checks.

## Wolfram Runtime

These skills assume a local Wolfram installation. Replace examples such as:

```powershell
& '<path-to-wolfram>\wolfram.exe' -script '<absolute-path-to-script.wl>'
```

with the actual path on your machine.

## Notes

- These skills are workflow templates. They do not include Wolfram/Mathematica itself.
- Generated derivation scripts should be run locally and verified with explicit checks before results are treated as reproduced.
- The paper proposition skill includes a style guide under `references/`, a runnable style exemplar under `examples/`, and a validator under `scripts/`.

## License

MIT License. See [LICENSE](LICENSE).
