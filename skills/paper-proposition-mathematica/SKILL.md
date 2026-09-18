---
name: paper-proposition-mathematica
description: Use when reproducing, checking, extending, or plotting economics paper propositions with Wolfram/Mathematica in a user-provided WL style-exemplar. Use for MFN/RPM/ET/NET/common-agency/game-theory models, symbolic equilibrium derivations, thresholds, regime restrictions, or any request to mimic a user's Mathematica code style, run step-by-step, avoid one-shot black-box scripts, or produce a human-readable `.wl` derivation.
---

# Paper Proposition Mathematica

For mathematical derivation or research-report tasks, read [the research and delivery requirements](references/research-delivery-rules.md). These define the derivation, coverage, reproducibility, and rendering requirements for the requested task. Apply only the parts relevant to the requested task; do not expand short explanations into a full research pipeline.

## Overview

Use this skill to write or revise Mathematica/Wolfram derivations that replicate theoretical economics paper propositions in the user's preferred style: style-exemplar `.wl`/notebook-code style, structured regime blocks, explicit intermediate outputs, scenario-level `Association` results, final `summaryRows`/`summaryGrid` comparison tables, and reproducible symbolic checks.

Before writing code, read [mathematica-style-guide.md](references/mathematica-style-guide.md). If the user provides or has previously identified a style-exemplar folder or file, inspect several representative files before generating the new derivation. Treat those code patterns as the highest-priority style source. If no user exemplar is provided, inspect the bundled default example [mfn-rpm-nonash-competition-style.wl](examples/mfn-rpm-nonash-competition-style.wl).

## Workflow

For report writing or revision, first read
[references/report-quality-gate.md](references/report-quality-gate.md).
Use its notation map and scenario/item inventory before generating the body,
not only after building a summary table. Run its contract validator when using
structured exports; retain manual semantic review for unregistered formulas.
This report gate is separate from the WL style/runtime gate below.

1. Fix the original model, decision variables, timing, strategy/feasible sets, parameter domain and conclusion quantifiers from the existing task. Identify whether the target is an identity, conditional solution, local/global optimum, Nash, SPE or an audit. New assumptions must be explicit; do not silently alter the model.
2. Inspect the user's style-exemplar examples when available; otherwise inspect the bundled default example. Extract the active style: section comments, symbol names, full candidate lists and justified selection, `Association`, `summaryRows`, `summaryGrid`, and visible intermediate outputs.
3. Start from a `.wl` derivation outline with `ClearAll["Global`*"]`, `$Assumptions`, model primitives, and ordered economic blocks. Do not begin from final formulas or CSV exporters.
4. Run Mathematica step by step through small kernel inputs while deriving. After each major economic block, keep the output visible in the final `.wl` by leaving key expressions unsuppressed or by printing/echoing them. When using `wolfram.exe -noprompt` with piped input, set the output directory explicitly because `$InputFileName` is empty.
5. Build the model from primitives: utility or inverse demand, FOCs, solved demand functions `D1`, `D2`, and then regime-specific prices, quantities, profits, constraints, and equilibrium concepts.
6. Derive each regime in this order unless the paper requires otherwise: conditional retail responses, dealer/upstream FOCs, full candidates, justified selection, candidate values, domains/feasibility, appropriate optimality and deviation arguments, regime result `Association`. Strict Hessian negativity is not universally necessary. A FOC solution alone does not establish equilibrium.
7. Derive thresholds completely: write the binding equation, solve all roots, select the economically valid root with assumptions, derive nonnegativity/feasibility boundaries, prove threshold ordering, and solve the equilibrium inside each threshold region.
8. For repeated regimes, finish with `summaryRows` plus `summaryGrid = Grid[Prepend[summaryRows, headers], ...]`; for proposition thresholds, finish with `Delta...`/`Omega...` objects, region tables, and checks.
9. Use the user's names: `FOC...`, `foc...`, `sol...All`, `sol...`, `p1BR...`, `piU...`, `Wstar...`, `Mstar...`, `Collusion...`, `Mdev...`, `Delta...`, `Omega...`, and scenario suffixes such as `NoMFNNoRPM`, `MFNNoRPM`, `NoRPM`, `RPM`, `ET`, `NET`, and `AS`.
10. Preserve raw mathematical results and classify evidence as proved/refuted/unresolved relative to the exact statement, assumptions and quantifiers. Separately register nonempty technical `checks` of the form `{nonblank name, Boolean}`. `TrueQ[FullSimplify[claim, ass]]` may be used for a technical assertion, but False does not automatically refute the mathematical claim. Match evidence to the requested scope; use numeric benchmarks only when requested or needed.
11. Only after the stepwise derivation is complete, assemble the full style-exemplar `.wl` script; export CSV/check tables as secondary verification artifacts. Generate `.nb` only if the user explicitly requests it.
12. Run the completed script through the runtime validator below, saving command, output and exit status. This reproducibility run supplements the stepwise derivation.

## Style Rules

- Use separator comments for mature scripts, e.g. `(* ============================== *)`, `(* 0. Assumptions *)`, `(* Demand system *)`, `(* Profit functions *)`.
- Use explanatory comments and economic row labels in the user's preferred language; preserve Chinese labels when requested or part of the supplied exemplar.
- Keep paper objects visible in comments, for example `Pi^N_ET`, `Delta_NE`, and self-enforcement constraints.
- Preserve the compact Mathematica idiom: `FullSimplify[..., Assumptions -> $Assumptions]`, `Solve[...]`, `Reduce[...]`, justified selected rules, `D[..., var]`, `x /. sol`. No extraction token such as `First` is mandatory.
- Prefer explicit intermediate objects over one large expression. Future checks should be able to inspect each economic step.
- Preserve the paper's mathematical notation as Mathematica symbols. If the source uses Greek letters, the `.wl` derivation must use Wolfram Greek symbols such as `\[Theta]`, `\[Alpha]`, `\[Gamma]`, and related decorated notation where possible; the generated Mathematica output should display Greek mathematical objects, not English replacements.
- Do not use English aliases such as `theta`, `alpha`, `gamma`, `thetaHat`, `thetaBar`, `Ffun`, or `ffun` for core mathematical primitives when the source model uses θ, α, γ, θ-hat, `F(θ)`, or `f(θ)`.
- Keep stepwise derivation auditable: each major block must have visible input and output in the final `.wl`, either through notebook-style cells, unsuppressed symbolic objects, `Echo`, or an explicit transcript helper. Do not collapse the derivation into a one-shot batch script.
- When proving rankings, use `FullSimplify[expr, ass]`, plus `Factor[Together[...]]` so signs are inspectable.
- At key economic transformations, the agent must actively state the target form before moving on. Examples include inverse-hazard markup, Lerner/unit-margin expressions, threshold boundaries, envelope forms, and welfare rankings. Do not merely keep whatever shape `FullSimplify` returns. Convert the raw equation and the target equation into comparable residuals, record any nonzero multiplier assumption, and add a Boolean equivalence check.
- Collect final regime results as associations before building comparison tables.
- Use style-exemplar `.wl` output as the primary user-facing artifact: ordered section comments, visible key outputs, `Association`, `summaryRows`, `summaryGrid`, and concise economic comments. CSV exports are checks, not the main presentation.
- Do not force `.nb` generation. If `.nb` is requested, generate it only after the `.wl` derivation is correct.
- Do not introduce new shortcut symbols after model setup except standard calculus notation and variables already in the model. If an abbreviation is necessary, define it immediately in a comment and include an expansion/equality check.
- Do not hide threshold derivations behind a final formula. Show the binding equation, roots, selected root, feasibility restriction, and region-specific equilibrium.
- Derive from primitives before comparing benchmarks. Hand-entered expected results need a traceable source and a defined test purpose; never use them as circular derivation. Paper formulas may be labeled `paperClaim...`; independently established regression fixtures are legitimate. Variable names alone do not establish evidence quality.
- When numerical comparison is relevant, identify benchmark provenance and match the same branch and domain. Preserve all roots from `NSolve`; `FindRoot` finds a local root and does not prove completeness or uniqueness. Check residuals constructed from primitives before equations can evaluate to True/False.
- Be careful with Chinese strings in direct `wolfram.exe -script` on Windows. If direct script execution fails on encoding while stepwise `-noprompt` succeeds, keep the final `.wl` ASCII-only or encode Chinese labels with Wolfram escapes / `FromCharacterCode`.
- For full executable derivations, print/export a nonempty technical check table and fail on invalid rows or non-True results. Keep raw unresolved/refuted research evidence separately. A valid refutation may complete an audit; a required positive proof remains incomplete when unresolved.

## Bundled Example

Use [examples/mfn-rpm-nonash-competition-style.wl](examples/mfn-rpm-nonash-competition-style.wl) as the built-in default style exemplar when the user does not provide one. It demonstrates:

- package-style `.wl` converted from notebook code while remaining runnable;
- `ClearAll["Global`*"]`, `$Assumptions`, demand/profit primitives, and regime blocks;
- `p2BR...`, `piU...`, `foc...`, `sol...All`, justified singleton extraction, and regime `Association` objects;
- final `summaryRows4` and `summaryGrid4 = Grid[...]`;
- escaped Chinese labels that are stable under command-line Wolfram execution.

This is a conditional stationary-point/style example. Its FOC and structure checks do not prove nonnegative demand, global optimality or complete equilibrium over the original parameter domain. Object names are retained for compatibility.

## Common Mistakes

- Do not stop at plotting. A proposition replication needs symbolic equality checks and sign or ranking checks.
- Retain all branches. Use list-valued substitution intentionally; extract a branch only with its domain and rationale. Unknown feasibility must not be silently discarded by `Select[... TrueQ ...]`.
- Do not leave final results as scattered variables when comparing multiple regimes. Put each regime into an `Association`, then build `summaryRows`.
- Do not treat a formula matching the paper as proof that the proposition statement is true. Separately verify the ranking under assumptions.
- When expressions are homogeneous, normalize parameters only after documenting the mapping, for example `r = gamma/beta`.
- Do not start by writing a full `.wl` file and running it once as a black box. The workflow requires stepwise Mathematica derivation first, then a full style-exemplar `.wl` after the model is complete.
- Do not replace the user's naming style with generic names like `profitR1`, `retailSol`, or `HDealer` when the notebook pattern suggests names such as `pi...`, `foc...`, `sol...All`, `Wstar...`, `Mstar...`, `Delta...`, or `Omega...`.
- Do not put non-Boolean objects into the `checks` table. Bad examples include `{True, True, True}`, an `Association` of numeric benchmark values, a symbolic expression that has not simplified to `True`, or a raw table of outputs. Convert them to strict Boolean claims first, such as `TrueQ[FullSimplify[And @@ listOfBooleans, Assumptions -> ass]]` or `TrueQ[numericBenchmark == expectedBenchmark]`.
- Do not put raw `And @@ focChecks`, `And @@ consistencyClaims`, or unsimplified symbolic conditions directly into `checks`. These can evaluate to `ConditionalExpression[True, ...]` under Wolfram and will fail the Boolean gate. Use `TrueQ[FullSimplify[And @@ focChecks, Assumptions -> ass]]`.
- Do not allow the script to finish successfully when checks are malformed or false. A script that runs with exit code `0` while `checks` contains non-Boolean values is not verified.
- Do not let benchmarks substitute for derivation. Inspect provenance, independent evidence and primitive consistency, not whether a variable starts with `expected`.
- Do not make representative numeric benchmarks by guessing an `Association[...]` of expected values. A wrong hard-coded benchmark is not a derivation check. Compare symbolic results to an independently computed numeric solution, or check numeric residuals from the original FOCs.
- Do not skip economically meaningful algebraic rewrites just because Mathematica did not return them automatically. `FullSimplify` is a verifier and simplifier, not a substitute for the agent choosing the relevant economic target form and checking it by residual equivalence.

## WL Script Quality Gate

Inspect full derivations for the applicable items below. A focused identity check or conditional solution need not add unused regimes or a summary grid; required multi-regime deliverables retain full tables. Style-token presence does not prove mathematics:

- `ClearAll["Global`*"]` and `$Assumptions`;
- model primitives before any final result formula;
- regime blocks with comments, not a single compact export block;
- FOC/SOC objects and complete solution lists such as `sol...All`;
- retained candidates and justified selection, or an explicit complete relation from `Reduce`;
- regime result `Association` objects where applicable;
- final `summaryRows` and `summaryGrid = Grid[...]`;
- a nonempty technical `checks` table and separate evidence/status for required mathematical claims;
- a hard-fail block that first validates nonempty two-element named rows, then Boolean results and their conjunction;
- key symbolic results left visible in the script by not ending those lines with semicolons, matching the user's style-exemplar code;
- Mathematica Greek symbols for Greek source primitives, with no unexplained English aliases such as `thetaHat`, `Ffun`, or `ffun`;
- notebook-style input blocks, visible intermediate outputs, or an explicit transcript mechanism such as `show[step, input, output]`.
- explicit transformation checks for key economic rewrites, where the raw FOC/constraint residual and the target economic-form residual are shown and verified as equivalent under assumptions.

Use this verification block or an equivalent:

```wolfram
If[!ListQ[checks] || Length[checks] == 0 ||
   !AllTrue[checks, MatchQ[#, {_String, _}] &&
     StringLength[StringTrim[First[#]]] > 0 &],
   Print["CHECKS_EMPTY_OR_MALFORMED"]; Exit[1]
];
checkResults = Last /@ checks;
checksAreBoolean = VectorQ[checkResults, BooleanQ];
allChecksTrue = TrueQ[checksAreBoolean && And @@ checkResults];

If[! allChecksTrue,
   Print["CHECKS_FAILED_OR_MALFORMED"];
   Print[checks];
   Exit[1]
];
```

Run the final file once through [the runtime validator](scripts/validate_wl_derivation.py), using the actual executable and a task-specific work directory. After verifying the executable, use:

```powershell
python '<skill-directory>/paper-proposition-mathematica/scripts/validate_wl_derivation.py' '<absolute-path-to-script.wl>' --wolfram '<discovered-wolfram-executable>' --work-dir '<task-directory>/runtime' --timeout 180
```

The wrapper executes the file and checks a nonempty list of `{nonempty string, Boolean}` rows. Success requires the current run's unique completion marker and matching process status; `Exit[0]` inside the target is incomplete. A missing/unlaunchable runtime fails (4), execution failure fails (5), timeout fails (6); check failures use 21–26. Preserve the command, output, exit status and actual check scope. No second full run is needed when this run supplies the evidence.

Style tokens are advisory by default; `--strict-style` makes the same heuristic style check blocking (3), not mathematically authoritative. Explicit `--no-runtime` reports `TEXT_VALIDATION_OK` and `RUNTIME_VALIDATION_NOT_REQUESTED`; this does not establish execution. Missing runtime is not a successful fallback. `RUNTIME_VALIDATION_OK` and the compatibility alias `VALIDATION_OK` mean only that the registered technical assertions passed, not that every mathematical claim or an equilibrium was proved.
