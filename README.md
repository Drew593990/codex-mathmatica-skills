# Codex Mathmatica Skills

Codex skills matching the local `mathmatica-user` and `paper-proposition-mathematica` skill names. They are used for Wolfram/Mathematica-based mathematical modeling and economics paper proposition replication.

## Skills

- `mathmatica-user`: general Wolfram Language modeling, symbolic derivation, equilibrium solving, formula verification, and numeric simulation.
- `paper-proposition-mathematica`: economics paper proposition replication style, including step-by-step derivation, style-exemplar `.wl` output, threshold and regime solving, result associations, summary grids, and strict verification checks.

The spelling `mathmatica-user` is intentional because it matches the original skill trigger used in the local workflow.

## What Changed In v0.2.0

This release adds explicit economic formula transformation checks for Mathematica derivations:

- requires agents to actively state the target economic form at key transformations, such as inverse-hazard markup, unit-margin/Lerner expressions, threshold boundaries, envelope forms, and welfare rankings;
- requires raw FOC or constraint equations and target economic forms to be compared through residual-equivalence checks;
- records nonzero multiplier assumptions before multiplying equations;
- adds reusable Wolfram Language examples for inverse-hazard markup, ranking/sign inspection, and threshold-boundary derivations;
- clarifies that `FullSimplify` verifies algebraic equivalence but should not replace the agent's economic judgment about the target form.

The previous stable release is tagged as `v0.1.0`.

## What Changed In v0.1.0

The `paper-proposition-mathematica` skill now includes stricter quality gates:

- derives from model primitives before final formulas;
- keeps intermediate FOCs, SOC/Hessian checks, solution lists, selected rules, regime associations, and summary grids visible;
- forbids hand-entered `expected...Eq = Association[...]` answer tables unless clearly labeled as external paper claims;
- forbids hand-entered numeric benchmark answer tables;
- requires every `checks` result to be a strict Boolean `True` or `False`;
- hard-fails generated `.wl` scripts with `Exit[1]` when checks are false or malformed;
- includes `scripts/validate_wl_derivation.py` for text and runtime validation;
- includes a bundled default style example under `examples/`.

## Included Example And Validator

- Style example: [`skills/paper-proposition-mathematica/examples/mfn-rpm-nonash-competition-style.wl`](skills/paper-proposition-mathematica/examples/mfn-rpm-nonash-competition-style.wl)
- Validator: [`skills/paper-proposition-mathematica/scripts/validate_wl_derivation.py`](skills/paper-proposition-mathematica/scripts/validate_wl_derivation.py)
- Style guide: [`skills/paper-proposition-mathematica/references/mathematica-style-guide.md`](skills/paper-proposition-mathematica/references/mathematica-style-guide.md)

## Installation

Copy the desired skill folder into your Codex skills directory:

```powershell
Copy-Item -Recurse .\skills\mathmatica-user $env:CODEX_HOME\skills\
Copy-Item -Recurse .\skills\paper-proposition-mathematica $env:CODEX_HOME\skills\
```

If `CODEX_HOME` is not set, copy the folders into your local Codex skills directory manually.

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
