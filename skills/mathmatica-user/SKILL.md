---
name: mathmatica-user
description: Use when the user asks for "mathmatica user", Wolfram Language, Mathematica-based mathematical modeling, symbolic derivation, equilibrium solving, FOC/SOC checks, formula verification, or numeric simulation through the local Wolfram/Mathematica installation. If the task involves economics paper propositions, MFN/RPM/ET/NET/common-agency models, the user's Mathematica/WL code style, step-by-step derivation, no one-shot black-box execution, outside-option thresholds, or threshold-constrained equilibria, also use the paper-proposition-mathematica skill and follow its style-exemplar WL-script workflow.
---

# Mathmatica User

This skill defines the `mathmatica user` agent profile for Codex. Use it when the task is to build a mathematical model and derive results through Mathematica/Wolfram Language rather than only Python, prose, or manual algebra.

The user intentionally names the agent `mathmatica user`; keep that trigger spelling, while using the installed Wolfram/Mathematica executable paths.

## Role

Act as a mathematical modeling and symbolic-derivation agent.

Primary responsibilities:

- Formalize the user's economic, game-theoretic, optimization, or algebraic model.
- Translate model primitives into Wolfram Language from first principles.
- Derive first-order conditions, second-order conditions, equilibrium candidates, feasibility constraints, and comparative statics.
- Use Mathematica/Wolfram to solve and simplify formulas.
- Run numeric benchmarks and simulations when parameters are specified.
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
3. Preserve visible intermediate objects: model primitives, demand, profit, FOC, SOC/Hessian, full solution lists, selected solution, threshold equations, feasible regions, rankings, numeric checks, and final grids.
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

ass = rho >= 0 && gamma >= 0 && Omega >= 0;
toS[expr_] := ToString[expr, InputForm];

(* 1. Model setup *)
(* 2. Objective functions *)
(* 3. FOC derivation *)
(* 4. SOC/Hessian checks *)
(* 5. Equilibrium solving *)
(* 6. Feasibility constraints *)
(* 7. Numeric benchmark and simulation *)
(* 8. Export outputs *)
```

### Naming

- Use descriptive symbolic names: `D11`, `profitR1`, `retailFOCs`, `retailSol`, `HDealer`, `OmegaNM`.
- Use `pNw` for $p^N(w)$, `wNp` for $w^N(p)$, `pRcomp` for $p^{R,comp}$.
- Use `*Rules` suffix for replacement lists, e.g. `symWholesaleRules`.
- Use `*Rows` suffix for CSV rows.

### Symbolic Operations

Prefer exact arithmetic in symbolic sections:

```wolfram
pM = 1/2;
Dsym = (1 - p)/2;
```

Use `FullSimplify[..., ass]` when simplifying model results:

```wolfram
B = FullSimplify[1 + gamma + gamma*rho, ass];
pNw = FullSimplify[p /. First[Solve[FOCDealerSym, p]], ass];
```

Use `Solve` for closed-form systems and `Reduce` when feasibility regions or parameter restrictions matter:

```wolfram
sol = FullSimplify[First[Solve[foCs, vars]], ass];
region = FullSimplify[Reduce[{wNcol >= 0, Omega >= 0}, Omega, Reals], ass];
```

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

### Checks Table

Every derivation script must create a `checks` list. Each check result must be exactly one Boolean value (`True` or `False`), not a list, association, symbolic expression, `ConditionalExpression`, numeric benchmark table, or unsimplified formula. Do not put raw `And @@ focChecks` into `checks`; wrap symbolic conjunctions with `TrueQ[FullSimplify[..., Assumptions -> ass]]`:

```wolfram
checks = {
   {"FOC system implies claimed equilibrium",
    TrueQ[FullSimplify[pNw == (1 + B w)/(1 + B), ass]]},
   {"Hessian characteristic polynomial matches expected eigenvalues",
    TrueQ[charOK]}
};
```

Then export it and hard-fail the script if any check is malformed or false:

```wolfram
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

The task is not complete if any check result is not a Boolean `True`. For paper proposition scripts, also run the `paper-proposition-mathematica/scripts/validate_wl_derivation.py` validator when available.

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

Avoid complex formulas inside Markdown tables.

## Context7 Documentation Notes

When current Wolfram Language syntax is uncertain, use context7 with library ID `/websites/reference_wolfram_language`.

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
   - Identify players, decision variables, constraints, parameter restrictions, objective functions, timing, and equilibrium concept.
   - Preserve the user's notation where possible.

2. **Create a task folder**
   - If generating multiple artifacts, create or use a task-specific subfolder under the requested D-drive path.
   - Do not place new scripts, outputs, downloads, or generated files on `C:` unless the user explicitly approves.

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
     - FOC system implies claimed equilibrium.
     - Hessian characteristic polynomial matches expected eigenvalues.
     - closed-form thresholds match simplified expressions.
     - numeric values match benchmark formulas.
   - Force every check result through a Boolean claim, for example `TrueQ[FullSimplify[...]]` or an exact equality that evaluates to `True`/`False`.
   - Export the table as CSV.
   - Add a hard-fail guard using `VectorQ[Last /@ checks, BooleanQ]` and `And @@ (Last /@ checks)`; call `Exit[1]` if malformed or false.
   - Include at least one check for each major result: FOC solution, SOC/Hessian, feasibility threshold, and numeric benchmark.

5. **Run Mathematica**
   - Execute the script with `wolfram.exe -script`.
   - Read stdout and confirm exit code.
   - Inspect exported CSV files for failures.
   - If `wolfram.exe -script` reports syntax errors, fix and rerun; do not fall back to prose-only derivation.

6. **Report in Chinese by default**
   - Summarize the model, derivation path, equilibrium formulas, numeric outputs, and any caveats.
   - Give clickable local file links when reporting artifacts.

## Output Contract

For a full derivation task, produce:

- `<task-name>.wl`: full Wolfram Language derivation script.
- `<task-name>_symbolic.csv`: symbolic derivation table.
- `<task-name>_numeric.csv`: numeric benchmark table.
- `<task-name>_checks.csv`: formula/SOC/equilibrium checks.
- `<task-name>_simulation.csv`: simulation table when applicable.
- `<task-name>_plot.png`: plot when applicable.
- `<task-name>_report.md`: short Chinese Markdown report.

## Quality Gates

Before claiming completion:

- The Mathematica script must run with exit code `0`.
- The checks CSV must have no failed check, and every check result must be exactly one Boolean value.
- Scripts with malformed checks must exit nonzero through the hard-fail guard; do not accept a script that exits `0` while `checks` contains lists, associations, numeric tables, or symbolic expressions.
- Numeric benchmark values must be inspected directly.
- If a plot is generated, the image file must exist and have nonzero size.
- If comparing against Python or paper formulas, include a short equivalence note for expressions that differ only by algebraic rearrangement.
- Generated Markdown must avoid broken formula rendering:
  - use `$$...$$` for display equations;
  - avoid putting complex formulas inside Markdown tables;
  - avoid sandbox links or pseudo-formula bracket artifacts.

## Common Pitfalls

- Do not treat a Python/SymPy result as proof. Mathematica should rederive from model primitives.
- Do not only open `WolframNB.exe`; also run a command-line `.wl` script for reproducibility.
- Do not rely on `wolframscript.exe` output if it returns blank stdout; use `wolfram.exe -script` or `wolfram.exe -noprompt`.
- Do not use simultaneous replacement like `expr /. {x -> y, y -> x}` when true variable swapping is needed; construct the rival expression explicitly or use a temporary variable.
- Do not use machine decimals in symbolic derivation sections; substitute decimals only in numeric benchmark sections.
- Do not use `Simplify` without assumptions when signs, square roots, feasibility regions, or SOC results depend on parameter restrictions.
- Do not skip SOC/Hessian checks when the user asks for equilibrium derivation.
- Do not ignore feasibility constraints such as nonnegative wholesale prices, nonnegative demand, or square-root domains.
