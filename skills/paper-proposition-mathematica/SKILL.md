---
name: paper-proposition-mathematica
description: Use when reproducing, checking, extending, or plotting economics paper propositions with Wolfram/Mathematica scripts in the user's established notation and notebook style.
---

# Paper Proposition Mathematica

## Overview

Use this skill to write or revise Mathematica/Wolfram scripts that replicate theoretical economics paper propositions in the user's preferred style: structured regime blocks, scenario-level `Association` results, final `summaryRows` comparison tables, and reproducible symbolic checks.

Before writing code, read [mathematica-style-guide.md](references/mathematica-style-guide.md) for the naming rules, section-comment style, final result-list pattern, and command templates distilled from the user's Proposition 1 and MFN/RPM replication scripts.

## Workflow

1. Read the proposition and identify the regimes, variables, constraints, equilibrium objects, and target comparisons.
2. Start the script with `ClearAll["Global`*"]`, assumptions, output directory setup when exports are needed, and a `toS` helper for symbolic CSV output.
3. Build the model from primitives: utility or inverse demand, FOCs, solved demand functions `D1`, `D2`, and then regime-specific prices, quantities, and profits.
4. Derive each regime in this order unless the paper requires otherwise: retail best responses, upstream FOCs, `sol...All`, `sol... = First[...]`, then a regime-level result association such as `discEq`, `mfnEq`, or `NoMFNNoRPMEq`.
5. For repeated regimes, finish with `summaryRows` plus `summaryGrid = Grid[Prepend[summaryRows, headers], ...]`; for proposition thresholds, finish with `Delta...` objects and a checks table.
6. Use the user's names: `FOC...`, `foc...`, `sol...All`, `sol...`, `p1BR...`, `piU...`, `Wstar...`, `Mstar...`, `Collusion...`, `Mdev...`, `Delta...`, and scenario suffixes such as `NoMFNNoRPM`, `MFNNoRPM`, `ET`, `NET`, and `AS`.
7. Add checks before claiming success: formula equality to paper expressions, denominator positivity, feasible domains, inequality rankings, and representative numeric benchmarks.
8. Export artifacts into a task subfolder when producing multiple files: script, `*_checks.csv`, `*_symbolic.csv`, numeric grids, and plots.
9. Run with the local Wolfram kernel, prefer:

```powershell
& '<path-to-wolfram>\wolfram.exe' -script '<absolute-path-to-script.wl>'
```

## Style Rules

- Use separator comments for mature scripts, e.g. `(* ============================== *)`, `(* 0. Assumptions *)`, `(* Demand system *)`, `(* Profit functions *)`.
- Use concise explanatory comments, especially final row labels such as wholesale price, retail price, quantity, upstream profit, and dealer profit.
- Keep paper objects visible in comments, for example `Pi^N_ET`, `Delta_NE`, and self-enforcement constraints.
- Preserve the compact Mathematica idiom: `FullSimplify[..., Assumptions -> $Assumptions]`, `Solve[...]`, `First[solAll]`, `D[..., var]`, `x /. sol`.
- Prefer explicit intermediate objects over one large expression. Future checks should be able to inspect each economic step.
- When proving rankings, use `FullSimplify[expr, ass]`, plus `Factor[Together[...]]` so signs are inspectable.
- Collect final regime results as associations before building comparison tables.

## Common Mistakes

- Do not stop at plotting. A proposition replication needs symbolic equality checks and sign or ranking checks.
- Avoid replacing with an unsliced solution list such as `w1 /. sol` unless the list shape is intentional; usually use `sol[[1]]`.
- Do not leave final results as scattered variables when comparing multiple regimes. Put each regime into an `Association`, then build `summaryRows`.
- Do not treat a formula matching the paper as proof that the proposition statement is true. Separately verify the ranking under assumptions.
- When expressions are homogeneous, normalize parameters only after documenting the mapping, for example `r = gamma/beta`.
