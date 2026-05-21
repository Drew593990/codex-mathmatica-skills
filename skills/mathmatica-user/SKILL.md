---
name: mathmatica-user
description: Use when the user asks for "mathmatica user", Wolfram Language, Mathematica-based mathematical modeling, symbolic derivation, equilibrium solving, FOC/SOC checks, formula verification, or numeric simulation through the local Wolfram/Mathematica installation.
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
- Export reproducible artifacts: `.wl` script, symbolic CSV, numeric CSV, formula-check CSV, plots when useful, and a short Markdown report.

## Wolfram Runtime

Prefer a locally installed Wolfram executable. Set the path for the target machine before running scripts:

```powershell
<path-to-wolfram>\wolfram.exe
```

Common related executables:

```powershell
<path-to-wolfram>\WolframKernel.exe
<path-to-wolfram>\WolframNB.exe
<path-to-wolfram>\wolframscript.exe
```

When `wolframscript.exe` does not print command output reliably, prefer:

```powershell
& '<path-to-wolfram>\wolfram.exe' -script '<absolute-path-to-script.wl>'
```

For one-off checks, use:

```powershell
@'
2+2
Exit[]
'@ | & '<path-to-wolfram>\wolfram.exe' -noprompt
```

Use `WolframNB.exe` only when the user explicitly wants the notebook UI opened. Reproducible derivations must still be run through a `.wl` script.

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

Every derivation script must create a `checks` list:

```wolfram
checks = {
   {"FOC system implies claimed equilibrium",
    FullSimplify[pNw == (1 + B w)/(1 + B), ass]},
   {"Hessian characteristic polynomial matches expected eigenvalues",
    charOK}
};
```

Then export it:

```wolfram
checkRows = Join[
   {{"Check", "Result"}},
   ({#[[1]], ToString[#[[2]], InputForm]} & /@ checks)
];

Export[FileNameJoin[{scriptDir, "task_checks.csv"}], checkRows, "CSV",
   CharacterEncoding -> "UTF8"];
```

The task is not complete if any check result is not `True`.

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

Wolfram can have trouble parsing some non-ASCII strings in `.wl` files depending on file encoding and shell path handling. If a non-English report is required, either:

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

Context7 examples may be generic. Prefer local execution with `wolfram.exe` as the final authority for this machine.

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
   - Export the table as CSV.
   - Include at least one check for each major result: FOC solution, SOC/Hessian, feasibility threshold, and numeric benchmark.

5. **Run Mathematica**
   - Execute the script with `wolfram.exe -script`.
   - Read stdout and confirm exit code.
   - Inspect exported CSV files for failures.
   - If `wolfram.exe -script` reports syntax errors, fix and rerun; do not fall back to prose-only derivation.

6. **Report clearly**
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
- `<task-name>_report.md`: short Markdown report.

## Quality Gates

Before claiming completion:

- The Mathematica script must run with exit code `0`.
- The checks CSV must have no failed check.
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
