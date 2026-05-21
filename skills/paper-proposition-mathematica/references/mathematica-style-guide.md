# Mathematica Style Guide for Paper Proposition Replication

This reference captures a notebook/script style for reproducing economics paper propositions with Wolfram Language. It is designed for symbolic derivations, equilibrium checks, threshold comparisons, and clear final output tables.

## Script Skeleton

```wolfram
ClearAll["Global`*"];

scriptDir = If[StringQ[$InputFileName] && $InputFileName =!= "",
   DirectoryName[$InputFileName],
   Directory[]
];

outDir = FileNameJoin[{scriptDir, "prop_outputs"}];
If[! DirectoryQ[outDir], CreateDirectory[outDir]];

$Assumptions = \[Alpha] > 0 && \[Beta] > 0 &&
   \[Gamma] >= 0 && \[Beta] > \[Gamma];
ass = $Assumptions;
toS[expr_] := ToString[expr, InputForm];
```

For headless `.wl` scripts, ASCII variables such as `alpha`, `beta`, `gamma` are acceptable if comments map them to paper notation. For notebook-style work, prefer `\[Alpha]`, `\[Beta]`, `\[Gamma]` when that matches the source paper.

## Section Order

Use clear section blocks. English comments are preferred for open-source scripts.

```wolfram
(* Utility function: derive demand and inverse demand *)

(* 1. Compute the non-collusive equilibrium under ET *)
(* step 1. Build profit functions for the two downstream firms *)
(* step 2. Solve the upstream firms' optimization problem *)

(* 2. Solve wholesale prices and profits under collusion *)

(* 3. Compute firm i's best response when deviating under ET *)

(* 4. Compute the critical discount factor Delta_ET *)
```

For asymmetric regimes:

```wolfram
(* Asymmetric regime: one side follows ET, the other follows NET. *)
(* 1. Solve the non-cooperative equilibrium *)
(* 2. Compute the collusive equilibrium *)
(* 3. Compute both deviation payoffs and allocate collusive total profit with share x *)
```

## Mature MFN/RPM Style

Use separator comments for the mechanical model blocks:

```wolfram
(* ============================== *)
(* 0. Assumptions *)
(* ============================== *)

(* ============================== *)
(* Demand system *)
(* ============================== *)

(* ============================== *)
(* Profit functions *)
(* ============================== *)
```

Then use scenario comments for economic regimes:

```wolfram
(* Stage 1: U chooses w1,w2 *)
(* NoMFN + NoRPM *)
(* MFN + NoRPM *)
(* NoMFN + RPM *)
(* MFN + RPM *)
```

## Scenario Naming

Use compact names for final result objects:

```wolfram
discEq       (* NoMFN + NoRPM / discriminatory wholesale prices *)
mfnEq        (* MFN + NoRPM *)
discRPMEq    (* NoMFN + RPM *)
mfnRPMEq     (* MFN + RPM *)
```

For longer derivation objects, keep the full scenario in the name:

```wolfram
piUNoMFNNoRPM[w1_, w2_]
focNoMFNNoRPM
solNoMFNNoRPMAll
solNoMFNNoRPM = First[solNoMFNNoRPMAll]
```

The `sol...All` then `sol... = First[sol...All]` pattern is preferred over repeatedly indexing into a raw solution list.

## Regime Result Associations

At the end of each regime, collect all economically relevant objects into an `Association`.

```wolfram
discEq = Association[
  "w1" -> FullSimplify[w1 /. solNoMFNNoRPM, Assumptions -> $Assumptions],
  "w2" -> FullSimplify[w2 /. solNoMFNNoRPM, Assumptions -> $Assumptions],
  "p1" -> FullSimplify[p1FromW1[w1] /. solNoMFNNoRPM, Assumptions -> $Assumptions],
  "p2" -> FullSimplify[p2BRNoMFN[w1, w2] /. solNoMFNNoRPM, Assumptions -> $Assumptions],
  "q1" -> FullSimplify[q1[p1FromW1[w1], p2BRNoMFN[w1, w2]] /. solNoMFNNoRPM,
    Assumptions -> $Assumptions],
  "q2" -> FullSimplify[q2[p2BRNoMFN[w1, w2], p1FromW1[w1]] /. solNoMFNNoRPM,
    Assumptions -> $Assumptions],
  "piU" -> FullSimplify[piUNoMFNNoRPM[w1, w2] /. solNoMFNNoRPM,
    Assumptions -> $Assumptions],
  "pi2" -> FullSimplify[pi2[p2BRNoMFN[w1, w2], w2, p1FromW1[w1]] /. solNoMFNNoRPM,
    Assumptions -> $Assumptions],
  "pi1" -> 0
];
```

Use the same key order across regimes:

```wolfram
{"w1", "w2", "p1", "p2", "q1", "q2", "piU", "pi2", "pi1"}
```

If a profit is mechanically zero, write `"pi1" -> 0` or `"pi2" -> 0` directly instead of deriving a noisy zero expression.

## Final Output List and Grid

For multi-regime comparison, prefer a final `summaryRows` list plus a `summaryGrid`.

```wolfram
summaryRows4 = {
  {"Wholesale price (w1)", discEq["w1"], mfnEq["w1"], discRPMEq["w1"], mfnRPMEq["w1"]},
  {"Wholesale price (w2)", discEq["w2"], mfnEq["w2"], discRPMEq["w2"], mfnRPMEq["w2"]},
  {"Retail price (p1)", discEq["p1"], mfnEq["p1"], discRPMEq["p1"], mfnRPMEq["p1"]},
  {"Retail price (p2)", discEq["p2"], mfnEq["p2"], discRPMEq["p2"], mfnRPMEq["p2"]},
  {"Quantity (q1)", discEq["q1"], mfnEq["q1"], discRPMEq["q1"], mfnRPMEq["q1"]},
  {"Quantity (q2)", discEq["q2"], mfnEq["q2"], discRPMEq["q2"], mfnRPMEq["q2"]},
  {"Upstream profit (piU)", discEq["piU"], mfnEq["piU"], discRPMEq["piU"], mfnRPMEq["piU"]},
  {"Dealer profit (pi2)", discEq["pi2"], mfnEq["pi2"], discRPMEq["pi2"], mfnRPMEq["pi2"]},
  {"Dealer profit (pi1)", discEq["pi1"], mfnEq["pi1"], discRPMEq["pi1"], mfnRPMEq["pi1"]}
};

summaryGrid4 = Grid[
  Prepend[summaryRows4, {"Object", "NoMFN+NoRPM", "MFN+NoRPM", "NoMFN+RPM", "MFN+RPM"}],
  Frame -> All,
  ItemStyle -> Directive[14],
  Alignment -> {Left, Center, Center, Center, Center}
];

summaryGrid4
```

For two-regime or three-regime propositions, keep the same structure with shorter headers:

```wolfram
summaryRows = {
  {"Delta", deltaET, deltaAS, deltaNE},
  {"Deviation profit", MdevinETcoll, MdevAS, MdevinNETcoll},
  {"Punishment profit", MstarinET, MstarAS, MstarinNET}
};
summaryGrid = Grid[
  Prepend[summaryRows, {"Object", "ET", "AS", "NET"}],
  Frame -> All,
  ItemStyle -> Directive[14],
  Alignment -> {Left, Center, Center, Center}
];
summaryGrid
```

## Common Primitives

- `U`: utility or surplus function used to derive demand.
- `eq1`, `eq2`: FOCs from primitive utility or inverse demand.
- `solDemand`: solved demand system.
- `D1[p1_, p2_]`, `D2[p1_, p2_]`: direct demand functions.
- `p1`, `p2`: retail prices.
- `q1`, `q2`: quantities.
- `w1`, `w2`: wholesale prices.
- `T1`, `T2`: fixed fees or franchise fees.

## Regime Suffixes

- `ET`: exclusive territories.
- `NET`: non-exclusive territories.
- `AS`: asymmetric regime.
- `RPM`: resale price maintenance.
- `MFN`: most-favored-nation clause.

## Price, Quantity, and Profit Objects

Use regime suffixes:

```wolfram
p1ET[w1_, w2_]
p2ET[w1_, w2_]
q1ET[w1_, w2_]
q2ET[w1_, w2_]
M1ET[w1_, w2_]
M2ET[w1_, w2_]
```

For NET:

```wolfram
p1NET[w1_, w2_] := w1;
p2NET[w1_, w2_] := w2;
q1NET[w1_, w2_] := D1[p1NET[w1, w2], p2NET[w1, w2]] // Simplify;
M1NET[w1_, w2_] := q1NET[w1, w2]*p1NET[w1, w2] // Simplify;
```

## FOCs, Solutions, and Equilibrium Values

```wolfram
FOCM1w1inET = D[M1ET[w1, w2], w1];
FOCM2w2inET = D[M2ET[w1, w2], w2];
solMiFOCinET = Solve[{FOCM1w1inET == 0, FOCM2w2inET == 0}, {w1, w2}, Reals] // Simplify;

WstarinET = w1 /. solMiFOCinET[[1]] // Simplify;
MstarinET = M1ET[WstarinET, WstarinET] // Simplify;
```

Collusion and deviation:

```wolfram
CollusioninET[w1_, w2_] = M1ET[w1, w2] + M2ET[w1, w2] // Simplify;
FOCcolw1 = D[CollusioninET[w1, w2], w1] // Simplify;
FOCcolw2 = D[CollusioninET[w1, w2], w2] // Simplify;
solCollusioninET = Solve[{FOCcolw1 == 0, FOCcolw2 == 0}, {w1, w2}, Reals] // Simplify;

WstarinETcoll = w1 /. solCollusioninET[[1]] // Simplify;
MinETcoll = M1ET[WstarinETcoll, WstarinETcoll] // Simplify;

M1devETcoll[w1_] = M1ET[w1, WstarinETcoll] // Simplify;
FOCM1devETcoll = D[M1devETcoll[w1], w1] // Simplify;
soldevCollinET = Solve[FOCM1devETcoll == 0, w1, Reals] // Simplify;
WstarindevETcoll = w1 /. soldevCollinET[[1]] // Simplify;
MdevinETcoll = M1ET[WstarindevETcoll, WstarinETcoll] // Simplify;
```

Threshold:

```wolfram
DeltaET = (MdevinETcoll - MinETcoll)/(MdevinETcoll - MstarinET) // Simplify;
```

## Asymmetric Sharing Pattern

Use `x` for the collusive-profit share and equalize the two incentive constraints.

```wolfram
Clear[x];
TotalCollAS = CollusionAS[W1colAS, W2colAS] // Simplify;
M1CollShareAS[x_] = x*TotalCollAS;
M2CollShareAS[x_] = (1 - x)*TotalCollAS;

Delta1AS[x_] := (M1devAS - M1CollShareAS[x])/(M1devAS - M1starAS) // FullSimplify;
Delta2AS[x_] := (M2devAS - M2CollShareAS[x])/(M2devAS - M2starAS) // FullSimplify;

solxAS = Solve[Delta1AS[x] == Delta2AS[x], x, Reals] // Simplify;
xStarAS = x /. solxAS[[1]] // FullSimplify;
DeltaAS = Delta1AS[x] /. x -> xStarAS // FullSimplify;
```

If a deviation optimum is at a boundary, document it explicitly:

```wolfram
(* Boundary deviation: with nonnegative wholesale price w1 >= 0, the optimum is w1 = 0. *)
W1devAS = 0;
```

## Commands to Prefer

- FOC: `D[profit, var] == 0`
- Closed-form systems: `Solve[eqs, vars, Reals] // Simplify`
- Strong simplification: `FullSimplify[expr, ass]`
- Inequality/ranking proof: `FullSimplify[deltaET < deltaNE, ass]`
- Sign inspection: `Factor[Together[deltaNE - deltaET]]`
- Feasible region: `Reduce[{constraints, expr > 0}, vars, Reals]`
- Numeric sanity check: `N[expr /. {\[Beta] -> 2, \[Gamma] -> 1}, 16]`
- Export symbolic rows: `Export[path, rows, "CSV", CharacterEncoding -> "UTF8"]`

## Verification Rows

Every serious replication script should export a checks table:

```wolfram
checks = {
   {"paper formula for Delta_ET reproduced",
    FullSimplify[DeltaET == claimedDeltaET, ass]},
   {"denominator of Delta_ET positive",
    FullSimplify[Denominator[Together[DeltaET]] > 0, ass]},
   {"ranking Delta_ET < Delta_NE",
    FullSimplify[DeltaET < DeltaNE, ass]}
};

checkRows = Join[
   {{"Check", "Result"}},
   ({#[[1]], toS[#[[2]]]} & /@ checks)
];

Export[FileNameJoin[{outDir, "proposition_checks.csv"}],
  checkRows, "CSV", CharacterEncoding -> "UTF8"];
```

## Plotting Defaults

When formulas are homogeneous in `beta` and `gamma`, plot against `r = gamma/beta`.

```wolfram
dET[r_] := FullSimplify[DeltaET /. {\[Beta] -> 1, \[Gamma] -> r}];

Plot[
 Evaluate[{dET[r], dAS[r], dNE[r]}],
 {r, 0, 0.999},
 Frame -> True,
 PlotLegends -> {"delta_ET", "delta_AS", "delta_NE"},
 GridLines -> {Range[0, 1, 0.1], Automatic},
 ImageSize -> 1050
]
```

Also export difference plots such as `delta_NE - delta_ET`, `delta_AS - delta_NE`, and `delta_AS - delta_ET`; these are often more informative than level plots.
