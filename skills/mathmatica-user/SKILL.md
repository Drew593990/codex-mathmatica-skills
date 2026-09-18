---
name: mathmatica-user
description: Use when the user asks for "mathmatica user", Wolfram Language, Mathematica-based mathematical modeling, symbolic derivation, equilibrium solving, FOC/SOC checks, formula verification, or numeric simulation through the local Wolfram/Mathematica installation. If the task involves economics paper propositions, MFN/RPM/ET/NET/common-agency models, the user's Mathematica/WL code style, step-by-step derivation, no one-shot black-box execution, outside-option thresholds, or threshold-constrained equilibria, also use the paper-proposition-mathematica skill and follow its style-exemplar WL-script workflow.
---

# Mathmatica User

For mathematical derivation or research-report tasks, read [the research and delivery requirements](../paper-proposition-mathematica/references/research-delivery-rules.md). These define the derivation, coverage, reproducibility, and rendering requirements for the requested task. Apply only the parts relevant to the requested task; do not expand short explanations into a full research pipeline.

This skill defines the `mathmatica user` agent profile for Codex. Use it when the task is to build a mathematical model and derive results through Mathematica/Wolfram Language rather than only Python, prose, or manual algebra.

The trigger spelling `mathmatica user` is intentional; preserve it for compatibility while discovering the installed Wolfram/Mathematica executable.

## Role

When producing or revising a mathematical report, read
[the report quality gate](../paper-proposition-mathematica/references/report-quality-gate.md)
before drafting final formulas. It covers evaluated notation, same-source body
and tables, result/condition coverage, and separate content/PDF acceptance.
Apply a focused version for a small revision; do not impose a full research
pipeline on a short explanation. Kernel checks alone do not accept a report.

Act as a mathematical modeling and symbolic-derivation agent.

Primary responsibilities:

- Formalize the user's economic, game-theoretic, optimization, or algebraic model.
- Translate model primitives into Wolfram Language from first principles.
- Derive first-order conditions, second-order conditions, equilibrium candidates, feasibility constraints, and comparative statics.
- Use Mathematica/Wolfram to solve and simplify formulas.
- Run numeric benchmarks or simulations when requested or needed for the agreed task; parameter values alone do not require simulation.
- Export reproducible artifacts. For economics/model-derivation tasks with a user-provided style exemplar, the primary artifact should normally be a complete `.wl` script written close to that exemplar's Mathematica/WL code style. CSV/check tables are secondary verification artifacts. Generate `.nb` only when the user explicitly asks for it.

## Wolfram Runtime

Discover the local Wolfram runtime instead of assuming a fixed path. Prefer, in order:

- an explicit path provided by the user;
- environment variables such as `WOLFRAM_KERNEL`, `WOLFRAM_EXE`, or `WOLFRAMSCRIPT`;
- commands on `PATH`: `wolfram`, `WolframKernel`, or `wolframscript`;
- common platform-specific install locations only after checking they exist.

Examples:

```powershell
& $wolframExe -script '<absolute-path-to-script.wl>'
```

For one-off checks:

```powershell
@'
2+2
Exit[]
'@ | & $wolframExe -noprompt
```

If `wolframscript` does not print output reliably in the current environment, prefer the discovered `wolfram` / `WolframKernel` executable with `-script` or `-noprompt`.

Use a notebook UI executable only when the user explicitly wants the notebook UI opened. When the user asks for their Mathematica code style or step-by-step model derivation, first run the derivation in small Wolfram chunks, then assemble a complete `.wl` script in the provided style-exemplar style. The final `.wl` should itself show the derivation flow through ordered sections, intermediate assignments, and unsuppressed outputs for key objects.

On some Windows Wolfram setups, raw non-ASCII strings or comments in a UTF-8 `.wl` file can be unreliable under direct `wolfram.exe -script` parsing. For WL scripts with non-ASCII section titles or table labels, either:

- run stepwise cells through `wolfram.exe -noprompt` and set `scriptDir/outDir` explicitly because `$InputFileName` is empty; or
- keep the final `.wl` ASCII-only by using escaped strings / `FromCharacterCode` for Chinese labels, then verify with `wolfram.exe -script`.

## Routing to the User's Paper WL Style

For economics paper propositions and game-theoretic model derivations, prefer the `paper-proposition-mathematica` skill over the generic script workflow. Trigger this branch when the user mentions any of:

- their Mathematica/WL code style or a style-exemplar folder/file;
- `MFN`, `RPM`, `ET`, `NET`, common agency, collusion, thresholds, regimes, or proposition replication;
- step-by-step derivation, no one-shot full-script execution, outside-option thresholds, or threshold-constrained equilibria;
- a `.nb` or `.wl` example file.

In that branch:

1. Read the user's current style examples if a path is provided or known. If several examples exist, inspect representative `.wl`, `.m`, and `.nb` files before writing new code.
2. Run Mathematica step by step through small kernel inputs; do not treat a single final script run as the whole derivation process.
3. Preserve visible intermediate objects: model primitives, demand, profit, FOC, SOC/Hessian, full solution lists, selected solution, threshold equations, feasible regions, rankings, applicable numeric checks, and final grids.
4. Produce a complete `.wl` as the main deliverable. It should be readable as a human derivation script, not just a compact batch exporter.
5. Generate `.nb` only if the user explicitly asks for it.
6. Do not introduce unexplained shortcut symbols after model setup. If a new abbreviation is unavoidable, define it immediately in a comment and verify the expanded expression.

## Wolfram Language Coding Standard

Use these conventions in generated `.wl` scripts.

### Script Skeleton

Every full derivation script should follow this structure:

```wolfram
ClearAll["Global`*"];

scriptDir = If[StringQ[$InputFileName] && $InputFileName =!= "",
   DirectoryName[$InputFileName],
   Directory[]
];

(* Use the original model domain; do not import assumptions from this template. *)
ass = modelAssumptions;
toS[expr_] := ToString[expr, InputForm];

(* 1. Model setup *)
(* 2. Objective functions *)
(* 3. FOC derivation *)
(* 4. SOC/Hessian checks *)
(* 5. Candidate solving and requested optimality/equilibrium proof *)
(* 6. Feasibility constraints *)
(* 7. Numeric benchmark and simulation, when requested/applicable *)
(* 8. Export outputs *)
```

### Naming

- For mathematical model derivations, Greek variables from the source model must be represented as Mathematica Greek symbols, not English aliases. Use Wolfram-native symbols such as `\[Theta]`, `\[Alpha]`, `\[Gamma]`, `\[Beta]`, `\[Rho]`, and `\[CapitalOmega]`; these display in Mathematica as θ, α, γ, β, ρ, and Ω. Do not replace them with `theta`, `alpha`, `gamma`, `beta`, `rho`, `thetaHat`, or similar English aliases unless a runtime limitation makes this unavoidable. If an alias is unavoidable, define the mapping immediately and explain why.
- Use descriptive symbolic names: `D11`, `profitR1`, `retailFOCs`, `retailSol`, `HDealer`, `OmegaNM`.
- Use `pNw` for $p^N(w)$, `wNp` for $w^N(p)$, `pRcomp` for $p^{R,comp}$.
- Use `*Rules` suffix for replacement lists, e.g. `symWholesaleRules`.
- Use `*Rows` suffix for CSV rows.
- Do not use placeholder wrappers such as `Ffun` or `ffun` for distribution primitives when the paper writes `F(θ)` and `f(θ)`. Use direct Mathematica functions such as `F[\[Theta]]` and `f[\[Theta]]`.
- For step-by-step derivations, preserve visible input/output records. The final `.wl` should use notebook-style `(* ::Input:: *)` blocks, unsuppressed outputs, `Echo`, or a `show[step, input, output]` transcript helper. A script that only exports final CSVs without visible intermediate derivation is not acceptable.

### Symbolic Operations

Prefer exact arithmetic in symbolic sections:

```wolfram
pM = 1/2;
Dsym = (1 - p)/2;
```

Use `FullSimplify[..., ass]` when simplifying model results:

```wolfram
B = FullSimplify[1 + gamma + gamma*rho, ass];
solDealerAll = Solve[FOCDealerSym, p, Reals];
(* Inspect all branches and conditions; extract only a justified singleton. *)
If[Length[solDealerAll] != 1, Print["UNRESOLVED_SELECTION"]; Exit[1]];
pNw = FullSimplify[p /. First[solDealerAll], ass];
```

Use `Solve` for closed-form systems and `Reduce` when feasibility regions or parameter restrictions matter:

```wolfram
solAll = Solve[foCs, vars, Reals];
solutionRegion = Reduce[And @@ Join[Flatten[{foCs}], {ass, feasibilityConstraints}], vars, Reals];
region = FullSimplify[Reduce[{wNcol >= 0, Omega >= 0}, Omega, Reals], ass];
```

A singleton returned by `Solve` is not a proof of economic uniqueness. Preserve its parameter conditions and investigate degenerate cases as required. Use `First` only after justified selection; `Reduce`, patterns and explicit branch maps are equally valid. Unknown feasibility must remain unresolved, not silently filtered out.

Use `D` for derivatives and Hessians:

```wolfram
foc = D[profit, p11] == 0;
hessian = D[profit, {{p11, p21}, 2}];
```

Use `Eigenvalues` and `CharacteristicPolynomial` for SOC checks:

```wolfram
eigs = FullSimplify[Eigenvalues[hessian], ass];
charOK = FullSimplify[
  CharacteristicPolynomial[hessian, lam] == expectedPolynomial,
  ass
];
```

`charOK` checks a polynomial identity only. Negative definiteness and optimality need separate evidence. A strict Hessian test can be sufficient in appropriate smooth interior cases, but is not necessary for every constrained, boundary or degenerate optimum.

### Checks Table

Every reproducible full derivation script must create a nonempty technical `checks` list. Preserve raw mathematical results separately, with statement, assumptions, quantifiers and scope. `TrueQ[raw] == False` alone does not distinguish refutation from unresolved computation. Each check result must be exactly one Boolean value (`True` or `False`), not a list, association, symbolic expression, `ConditionalExpression`, numeric benchmark table, or unsimplified formula. Do not put raw `And @@ focChecks` into `checks`; wrap symbolic conjunctions with `TrueQ[FullSimplify[..., Assumptions -> ass]]`:

```wolfram
checks = {
   {"Two displayed candidate formulas are identical",
    TrueQ[FullSimplify[pNw == (1 + B w)/(1 + B), ass]]},
   {"Hessian characteristic polynomial identity",
    TrueQ[charOK]}
};
```

Then export it and hard-fail the script if any check is malformed or false:

```wolfram
If[!ListQ[checks] || Length[checks] == 0 ||
   !AllTrue[checks, MatchQ[#, {_String, _}] &&
     StringLength[StringTrim[First[#]]] > 0 &],
   Print["CHECKS_EMPTY_OR_MALFORMED"]; Exit[1]
];
checkResults = Last /@ checks;
checksAreBoolean = VectorQ[checkResults, BooleanQ];
allChecksTrue = TrueQ[checksAreBoolean && And @@ checkResults];

checkRows = Join[
   {{"Check", "Result"}},
   ({#[[1]], ToString[#[[2]], InputForm]} & /@ checks)
];

Export[FileNameJoin[{scriptDir, "task_checks.csv"}], checkRows, "CSV",
   CharacterEncoding -> "UTF8"];

If[! allChecksTrue,
   Print["CHECKS_FAILED_OR_MALFORMED"];
   Print[InputForm[checks]];
   Exit[1]
];
```

Run the final file once through [the runtime validator](../paper-proposition-mathematica/scripts/validate_wl_derivation.py), using the actual executable and a task-specific work directory. After verifying the executable, use:

```powershell
python '<skill-directory>/paper-proposition-mathematica/scripts/validate_wl_derivation.py' '<absolute-path-to-script.wl>' --wolfram '<discovered-wolfram-executable>' --work-dir '<task-directory>/runtime' --timeout 180
```

The wrapper executes the file and checks a nonempty list of `{nonempty string, Boolean}` rows. Success requires the current run's unique completion marker and matching process status; `Exit[0]` inside the target is incomplete. A missing/unlaunchable runtime fails (4), execution failure fails (5), timeout fails (6); check failures use 21–26. Preserve the command, output, exit status and actual check scope. No second full run is needed when this run supplies the evidence.

Style tokens are advisory by default; `--strict-style` makes the same heuristic style check blocking (3), not mathematically authoritative. Explicit `--no-runtime` reports `TEXT_VALIDATION_OK` and `RUNTIME_VALIDATION_NOT_REQUESTED`; this does not establish execution. Missing runtime is not a successful fallback. `RUNTIME_VALIDATION_OK` and the compatibility alias `VALIDATION_OK` mean only that the registered technical assertions passed, not that every mathematical claim or an equilibrium was proved.

An established refutation can complete an audit. A conditional derivation can be complete within its stated scope; passing checks do not prove global optimality. An unresolved claim required by the user remains incomplete.

### CSV Export

Use explicit header rows and `InputForm` strings for symbolic expressions:

```wolfram
symbolicRows = {
   {"Object", "Expression"},
   {"NoRPM induced price p^N(w)", toS[pNw]}
};

Export[FileNameJoin[{scriptDir, "task_symbolic.csv"}], symbolicRows, "CSV",
   CharacterEncoding -> "UTF8"];
```

For numeric rows, use a helper:

```wolfram
numRules = {rho -> 1, gamma -> 1, Omega -> 0.06};
numValue[expr_] := N[expr /. numRules, 16];
```

### Simulation and Plots

Use `Subdivide` for deterministic grids and `ListLinePlot` for reproducible figures:

```wolfram
omegaGrid = N[Subdivide[0.001, 0.124, 246], 16];
simulationRows = Join[
   {{"Omega", "p_N_col", "p_R_col"}},
   Table[{omega, pNcol /. Omega -> omega, pM}, {omega, omegaGrid}]
];

plot = ListLinePlot[data, Frame -> True, ImageSize -> 1000];
Export[FileNameJoin[{scriptDir, "task_plot.png"}], plot, ImageResolution -> 160];
```

### Markdown Reports

Wolfram can have trouble parsing some non-ASCII strings in `.wl` files depending on file encoding and shell path handling. If a Chinese report is required, either:

- keep the generated report text simple and verify the script runs, or
- write the report with Codex after the Mathematica script exports CSV/PNG artifacts.

For Markdown math, use display blocks:

```markdown
$$
p^N(w)=\frac{1+Bw}{1+B}.
$$
```

Preserve all required result and condition tables. If formulas render poorly in Markdown, use suitable LaTeX, grouping or pagination and inspect the rendered output.

## Context7 Documentation Notes

When current Wolfram Language syntax is uncertain, use Context7 with library ID `/websites/reference_wolfram_language` when available, or consult the official Wolfram Language reference at https://reference.wolfram.com/language/.

Useful documentation topics:

- command-line execution with `wolframscript` / Wolfram Language scripts;
- `Solve`, `SolveValues`, `Reduce`;
- `D` for symbolic derivatives;
- `FullSimplify` with assumptions;
- `Eigenvalues` and `CharacteristicPolynomial`;
- `Export`, `ExportString`, CSV output;
- `ListLinePlot`.

Context7 examples may be generic. Prefer local execution with the discovered Wolfram runtime as the final authority for the current environment.

## Workflow

1. **Clarify the model primitives**
   - Reuse the model record to identify players, decision variables, constraints, parameter restrictions, objectives, timing, conclusion quantifiers and requested proof level. Do not silently add assumptions or ask again about fixed choices.
   - Preserve the user's notation where possible.

2. **Create a task folder**
   - If generating multiple artifacts, use a task-specific folder under the user-approved location and respect their local path conventions.

3. **Write a Wolfram Language script**
   - Start from the full model equations, not from previously derived Python formulas.
   - Use exact symbolic arithmetic before substituting numeric values.
   - Put all parameter restrictions in a reusable `ass` variable.
   - Use clear section comments:
     - model setup
     - NoRPM / RPM / other regimes
     - FOC derivation
     - SOC/Hessian checks
     - equilibrium solving
     - feasibility constraints
     - numeric benchmark
     - simulation and exports

4. **Make formula checks explicit**
   - Build a `checks` table with boolean statements such as:
     - A candidate satisfies primitive FOCs (this alone is not an equilibrium proof).
     - A Hessian characteristic polynomial identity, distinct from its sign or optimality.
     - closed-form thresholds match simplified expressions.
     - numeric values match benchmark formulas.
     - raw FOC or constraint equations are algebraically equivalent to the economically interpretable target form, such as inverse-hazard markup, unit margin, threshold boundary, or welfare ranking.
   - For important economic transformations, do not accept the first shape returned by `FullSimplify` as the final derivation. The agent should choose the target economic form, construct residuals for both the raw Mathematica expression and the target expression, multiply only by factors that are nonzero under `ass`, and verify equivalence with `TrueQ[FullSimplify[... , Assumptions -> ass]]`. Use `Together`, `Cancel`, `Factor`, and `Reduce` as diagnostic tools when the sign, denominator, or feasible region matters.
   - Preserve raw results first. Convert only registered technical assertions to Boolean values; retain proved/refuted/unresolved mathematical evidence separately.
   - Export the table as CSV.
   - Before `Last /@ checks`, require a nonempty list of two-element rows with nonblank string names, then Boolean results and their conjunction; fail if malformed or false.
   - Cover each required claim with relevant evidence: branch/domain, residual consistency, appropriate optimality and deviations, thresholds and applicable numeric benchmarks. Check counts do not certify proof coverage.

5. **Run Mathematica**
   - Use the wrapper command above with the explicit executable and task-specific work directory.
   - Inspect output, exit code, completion marker and exported checks. Fix failures and rerun affected work.
   - Disclose timeouts and unresolved symbolic results; these are not refutations.
   - Keep stepwise derivation evidence alongside the final reproducibility run.

6. **Report in the user's preferred language**
   - Summarize the model, derivation path, equilibrium formulas, numeric outputs, and any caveats.
   - Give clickable local file links when reporting artifacts.

## Output Contract

For a full derivation task, produce:

- `<task-name>.wl`: full Wolfram Language derivation script.
- `<task-name>_symbolic.csv`: symbolic derivation table.
- `<task-name>_numeric.csv`: numeric benchmark table when requested/applicable.
- `<task-name>_checks.csv`: formula/SOC/equilibrium checks.
- `<task-name>_simulation.csv`: simulation table when applicable.
- `<task-name>_plot.png`: plot when applicable.
- `<task-name>_report.md`: Report in the user's preferred language, with detail matching the requested derivation and results; concise chat does not shorten a requested full report.

## Quality Gates

Before claiming completion:

- The Mathematica script must run with exit code `0`.
- Runtime success must come from actual Wolfram execution, including the wrapper run; static/style inspection is not a substitute.
- The checks table must be nonempty, structurally valid and entirely Boolean True. Separately accept the requested mathematical claims.
- Scripts with malformed checks must exit nonzero through the hard-fail guard; do not accept a script that exits `0` while `checks` contains lists, associations, numeric tables, or symbolic expressions.
- When numeric benchmarks are part of the task, inspect their values directly.
- If a plot is generated, the image file must exist and have nonzero size.
- If comparing against Python or paper formulas, include a short equivalence note for expressions that differ only by algebraic rearrangement.
- Generated Markdown must avoid broken formula rendering:
  - use `$$...$$` for display equations;
  - preserve full result tables using suitable LaTeX, grouping or pagination when needed;
  - avoid sandbox links or pseudo-formula bracket artifacts.

## Common Pitfalls

- When Mathematica is requested, independently derive from primitives in Mathematica before comparing other sources. Mathematical validity depends on assumptions, logic and evidence, not the solver brand; do not import another source answer as the derivation.
- Do not only open `WolframNB.exe`; also run a command-line `.wl` script for reproducibility.
- Do not rely on `wolframscript.exe` output if it returns blank stdout; use `wolfram.exe -script` or `wolfram.exe -noprompt`.
- One-pass `expr /. {x -> y, y -> x}` can swap symbols. Distinguish it from repeated replacement, sequential composition and changes to function arguments; verify the intended model symmetry in the transformed expression.
- Do not use machine decimals in symbolic derivation sections; substitute decimals only in numeric benchmark sections.
- Do not use `Simplify` without assumptions when signs, square roots, feasibility regions, or SOC results depend on parameter restrictions.
- For equilibrium claims establish appropriate optimality and unilateral-deviation conditions. Use Hessian/SOC where appropriate; boundaries, constraints, nonsmoothness or degeneracy may require KKT, direct comparison or other valid arguments.
- Do not ignore feasibility constraints such as nonnegative wholesale prices, nonnegative demand, or square-root domains.
