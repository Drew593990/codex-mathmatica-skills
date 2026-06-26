---
name: paper-proposition-mathematica
description: Use when reproducing, checking, extending, or plotting economics paper propositions with Wolfram/Mathematica in a user-provided WL style-exemplar. Use for MFN/RPM/ET/NET/common-agency/game-theory models, symbolic equilibrium derivations, thresholds, regime restrictions, or any request to mimic a user's Mathematica code style, run step-by-step, avoid one-shot black-box scripts, or produce a human-readable `.wl` derivation.
---

# Paper Proposition Mathematica

## Overview

Use this skill to write or revise Mathematica/Wolfram derivations that replicate theoretical economics paper propositions in the user's preferred style: style-exemplar `.wl`/notebook-code style, structured regime blocks, explicit intermediate outputs, scenario-level `Association` results, final `summaryRows`/`summaryGrid` comparison tables, and reproducible symbolic checks.

Before writing code, read [mathematica-style-guide.md](references/mathematica-style-guide.md). If the user provides or has previously identified a style-exemplar folder or file, inspect several representative files before generating the new derivation. Treat those code patterns as the highest-priority style source. If no user exemplar is provided, inspect the bundled default example [mfn-rpm-nonash-competition-style.wl](examples/mfn-rpm-nonash-competition-style.wl).

## Workflow

1. Read the proposition and identify the regimes, variables, constraints, equilibrium objects, and target comparisons.
2. Inspect the user's style-exemplar examples when available; otherwise inspect the bundled default example. Extract the active style: section comments, symbol names, `sol...All`/`First @ ...` pattern, `Association`, `summaryRows`, `summaryGrid`, and visible intermediate outputs.
3. Start from a `.wl` derivation outline with `ClearAll["Global`*"]`, `$Assumptions`, model primitives, and ordered economic blocks. Do not begin from final formulas or CSV exporters.
4. Run Mathematica step by step through small kernel inputs while deriving. After each major economic block, keep the output visible in the final `.wl` by leaving key expressions unsuppressed or by printing/echoing them. When using `wolfram.exe -noprompt` with piped input, set the output directory explicitly because `$InputFileName` is empty.
5. Build the model from primitives: utility or inverse demand, FOCs, solved demand functions `D1`, `D2`, and then regime-specific prices, quantities, profits, constraints, and equilibrium concepts.
6. Derive each regime in this order unless the paper requires otherwise: retail best responses, dealer/upstream FOCs, Hessian/SOC, `sol...All`, `sol... = First @ sol...All`, candidate equilibrium values, feasibility restrictions, regime result `Association`.
7. Derive thresholds completely: write the binding equation, solve all roots, select the economically valid root with assumptions, derive nonnegativity/feasibility boundaries, prove threshold ordering, and solve the equilibrium inside each threshold region.
8. For repeated regimes, finish with `summaryRows` plus `summaryGrid = Grid[Prepend[summaryRows, headers], ...]`; for proposition thresholds, finish with `Delta...`/`Omega...` objects, region tables, and checks.
9. Use the user's names: `FOC...`, `foc...`, `sol...All`, `sol...`, `p1BR...`, `piU...`, `Wstar...`, `Mstar...`, `Collusion...`, `Mdev...`, `Delta...`, `Omega...`, and scenario suffixes such as `NoMFNNoRPM`, `MFNNoRPM`, `NoRPM`, `RPM`, `ET`, `NET`, and `AS`.
10. Add checks before claiming success: formula equality, denominator positivity, Hessian/SOC, feasible domains, threshold ordering, regime classification, inequality rankings, and representative numeric benchmarks. Every check result must be exactly one Boolean value, `True` or `False`; never store a list, association, symbolic expression, `ConditionalExpression`, or numeric benchmark object as a check result. Wrap symbolic claims as `TrueQ[FullSimplify[claim, Assumptions -> ass]]`.
11. Only after the stepwise derivation is complete, assemble the full style-exemplar `.wl` script; export CSV/check tables as secondary verification artifacts. Generate `.nb` only if the user explicitly requests it.
12. Run with a discovered local Wolfram kernel, for example:

```powershell
& $wolframExe -script '<absolute-path-to-script.wl>'
```

## Wolfram Runtime Discovery

Discover the local Wolfram runtime instead of assuming a fixed path. Prefer, in order:

- an explicit path provided by the user;
- environment variables such as `WOLFRAM_KERNEL`, `WOLFRAM_EXE`, or `WOLFRAMSCRIPT`;
- commands on `PATH`, such as `wolfram`, `WolframKernel`, or `wolframscript`;
- common platform-specific install locations only after checking they exist.

If `wolframscript` does not print output reliably, prefer `wolfram` or `WolframKernel` with `-script` or `-noprompt`.

## Style Rules

- Use separator comments for mature scripts, e.g. `(* ============================== *)`, `(* 0. Assumptions *)`, `(* Demand system *)`, `(* Profit functions *)`.
- Use explanatory comments in the user's preferred language, especially final row labels such as wholesale price, retail price, quantity, upstream profit, and dealer profit. If the user communicates in Chinese, prefer Chinese economic labels.
- Keep paper objects visible in comments, for example `Pi^N_ET`, `Delta_NE`, and self-enforcement constraints.
- Preserve the compact Mathematica idiom: `FullSimplify[..., Assumptions -> $Assumptions]`, `Solve[...]`, `First[solAll]`, `D[..., var]`, `x /. sol`.
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
- Do not create a table such as `expected...Eq = Association[...]` that hand-enters every final equilibrium object unless the user supplied those formulas as an explicit paper/proposition benchmark. For self-contained derivations, checks should verify the solved objects against the model primitives, FOCs, SOCs, substitutions, and feasibility conditions. If comparing to paper formulas, name the block `paperClaim...`, place it after the derived result, and state in comments that it is an external benchmark, not the derivation source.
- Do not hand-enter numeric benchmark associations such as `numericBenchmark == Association["p1" -> ...]` unless those numbers come from a user-supplied paper table and are labeled as `paperNumericClaim...`. For self-contained tests, derive numeric checks from independent numeric solving (`NSolve`/`FindRoot`) or verify that numeric substitutions satisfy the primitive FOCs, quantities, profits, and feasibility restrictions.
- If the user needs Chinese labels, be careful with Chinese strings in direct `wolfram.exe -script` on Windows. If direct script execution fails on encoding while stepwise `-noprompt` succeeds, keep the final `.wl` ASCII-only or encode Chinese labels with Wolfram escapes / `FromCharacterCode`.
- Build a hard-fail check block into every generated `.wl`: export or print the checks, verify each check result is a Boolean, and call `Exit[1]` when any check is not exactly `True`.

## Bundled Example

Use [examples/mfn-rpm-nonash-competition-style.wl](examples/mfn-rpm-nonash-competition-style.wl) as the built-in default style exemplar when the user does not provide one. It demonstrates:

- package-style `.wl` converted from notebook code while remaining runnable;
- `ClearAll["Global`*"]`, `$Assumptions`, demand/profit primitives, and regime blocks;
- `p2BR...`, `piU...`, `foc...`, `sol...All`, `First @ ...`, and regime `Association` objects;
- final `summaryRows4` and `summaryGrid4 = Grid[...]`;
- escaped Chinese labels that are stable under command-line Wolfram execution.

## Common Mistakes

- Do not stop at plotting. A proposition replication needs symbolic equality checks and sign or ranking checks.
- Avoid replacing with an unsliced solution list such as `w1 /. sol` unless the list shape is intentional; usually use `sol[[1]]`.
- Do not leave final results as scattered variables when comparing multiple regimes. Put each regime into an `Association`, then build `summaryRows`.
- Do not treat a formula matching the paper as proof that the proposition statement is true. Separately verify the ranking under assumptions.
- When expressions are homogeneous, normalize parameters only after documenting the mapping, for example `r = gamma/beta`.
- Do not start by writing a full `.wl` file and running it once as a black box. The workflow requires stepwise Mathematica derivation first, then a full style-exemplar `.wl` after the model is complete.
- Do not replace the user's naming style with generic names like `profitR1`, `retailSol`, or `HDealer` when the notebook pattern suggests names such as `pi...`, `foc...`, `sol...All`, `Wstar...`, `Mstar...`, `Delta...`, or `Omega...`.
- Do not put non-Boolean objects into the `checks` table. Bad examples include `{True, True, True}`, an `Association` of numeric benchmark values, a symbolic expression that has not simplified to `True`, or a raw table of outputs. Convert them to strict Boolean claims first, such as `TrueQ[FullSimplify[And @@ listOfBooleans, Assumptions -> ass]]` or `TrueQ[numericBenchmark == expectedBenchmark]`.
- Do not put raw `And @@ focChecks`, `And @@ consistencyClaims`, or unsimplified symbolic conditions directly into `checks`. These can evaluate to `ConditionalExpression[True, ...]` under Wolfram and will fail the Boolean gate. Use `TrueQ[FullSimplify[And @@ focChecks, Assumptions -> ass]]`.
- Do not allow the script to finish successfully when checks are malformed or false. A script that runs with exit code `0` while `checks` contains non-Boolean values is not verified.
- Do not make the verification section look like the derivation by assigning a full answer table named `expected...Eq`, `expected...Results`, or similar. That pattern can mask a skipped derivation. Use primitive-consistency checks instead, or use clearly labeled `paperClaim...` formulas only when they come from the paper/proposition being replicated.
- Do not make representative numeric benchmarks by guessing an `Association[...]` of expected values. A wrong hard-coded benchmark is not a derivation check. Compare symbolic results to an independently computed numeric solution, or check numeric residuals from the original FOCs.
- Do not skip economically meaningful algebraic rewrites just because Mathematica did not return them automatically. `FullSimplify` is a verifier and simplifier, not a substitute for the agent choosing the relevant economic target form and checking it by residual equivalence.

## WL Script Quality Gate

Before reporting completion, inspect the generated `.wl` file. At minimum it must contain:

- `ClearAll["Global`*"]` and `$Assumptions`;
- model primitives before any final result formula;
- regime blocks with comments, not a single compact export block;
- FOC/SOC objects and complete solution lists such as `sol...All`;
- selected rules such as `sol... = First @ sol...All` or `rules = First @ sol...`;
- regime result `Association` objects where applicable;
- final `summaryRows` and `summaryGrid = Grid[...]`;
- a `checks` table with all major claims verified;
- a hard-fail block that requires `VectorQ[Last /@ checks, BooleanQ]` and `And @@ (Last /@ checks)`;
- key symbolic results left visible in the script by not ending those lines with semicolons, matching the user's style-exemplar code;
- Mathematica Greek symbols for Greek source primitives, with no unexplained English aliases such as `thetaHat`, `Ffun`, or `ffun`;
- notebook-style input blocks, visible intermediate outputs, or an explicit transcript mechanism such as `show[step, input, output]`.
- explicit transformation checks for key economic rewrites, where the raw FOC/constraint residual and the target economic-form residual are shown and verified as equivalent under assumptions.

Use this verification block or an equivalent:

```wolfram
checkResults = Last /@ checks;
checksAreBoolean = VectorQ[checkResults, BooleanQ];
allChecksTrue = TrueQ[checksAreBoolean && And @@ checkResults];

If[! allChecksTrue,
   Print["CHECKS_FAILED_OR_MALFORMED"];
   Print[checks];
   Exit[1]
];
```

When Python >= 3.9 and a Wolfram runtime are both available, run [scripts/validate_wl_derivation.py](scripts/validate_wl_derivation.py) on the generated `.wl` before reporting completion. This validates style tokens, hard-fail logic, and sometimes runtime `checks`. If Python is unavailable, skip the validator and rely on direct Wolfram runtime verification.

Do not treat the validator as the authoritative runtime proof. If it prints `RUNTIME_VALIDATION_SKIPPED`, cannot discover Wolfram, or only reports text validation, run the `.wl` yourself with the explicit discovered or user-provided executable path, for example `& $wolframExe -script '<file.wl>'`. Completion requires exit code `0`, the script's success marker such as `ALL_CHECKS_TRUE`, and exported checks showing Boolean `True` rows.
