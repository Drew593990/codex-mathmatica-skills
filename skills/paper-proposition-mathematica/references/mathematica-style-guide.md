# Mathematica Style Guide for Paper Proposition Replication

This guide captures a reusable Mathematica workflow for economics/game-theory paper derivations. The priority is a human-readable `.wl` derivation script that looks close to the user's provided style examples: ordered economic sections, explicit intermediate objects, visible symbolic outputs, `Association`, and final `Grid` summaries. A `.nb` is optional and should be generated only when the user asks for it.

## Style-Exemplar WL Protocol

For the user's model derivation tasks:

1. Inspect representative style-exemplar files when available. If the user gives a folder, sample several `.wl`, `.m`, and `.nb` files, prioritizing files whose names or contents match the current model family.
2. Run Mathematica step by step with small kernel inputs while deriving. Do not treat a single final script run as the whole derivation process.
3. Assemble a complete `.wl` script after the derivation is clear. The `.wl` is the main artifact.
4. Keep the output of each economic step visible in the `.wl` style: FOC, solution list, selected solution, threshold equation, threshold roots, feasible region, `Association`, and final `Grid`.
5. Export CSV/check tables only as verification artifacts. Generate `.nb` only when explicitly requested.

If no user-provided style exemplar is available, use the bundled default example `examples/mfn-rpm-nonash-competition-style.wl`. It is a runnable `.wl` script that preserves notebook-code style without requiring a `.nb` file.

When stepwise input is piped through `wolfram.exe -noprompt`, set the output folder explicitly because `$InputFileName` is empty. On Windows, direct `wolfram.exe -script` can be unreliable for raw Chinese strings in UTF-8 `.wl` files; if this happens, keep the `.wl` ASCII-only or encode Chinese labels with Wolfram escapes / `FromCharacterCode`.

## WL Script Must Match the Style Exemplar

The `.wl` is the main deliverable unless the user explicitly asks for `.nb`. Do not produce a compact batch exporter as the main script. The script should read like the user's provided Mathematica/WL examples:

- begin with `ClearAll["Global`*"];`;
- define `$Assumptions` early;
- use section comments and step comments;
- define functions with patterns, e.g. `piUDisc[w1_, w2_] := ...`;
- derive FOCs explicitly, e.g. `focDisc = {...}`;
- solve full systems, e.g. `solDiscW = FullSimplify[Solve[focDisc, {w1, w2}], Assumptions -> $Assumptions]`;
- select rules explicitly, e.g. `discRules = First @ solDiscW`;
- collect regime results into `discEq`, `mfnEq`, `discRPMEq`, `mfnRPMEq`, or analogous `Association` objects;
- build `summaryRows` and `summaryGrid = Grid[...]`;
- put `summaryGrid` on its own final line without a semicolon;
- leave key objects unsuppressed, matching the notebook code style.

The bundled default example uses this same pattern. In particular, copy its high-level structure rather than its economic content: assumptions, primitives, one block per regime, FOC solving, `Association` result objects, and final `summaryGrid`.

Use this style check before completion:

```wolfram
wlText = Import[wlPath, "Text"];
wlStyleChecks = {
  StringContainsQ[wlText, "ClearAll[\"Global`*\"]"],
  StringContainsQ[wlText, "$Assumptions"],
  StringContainsQ[wlText, "FullSimplify"],
  StringContainsQ[wlText, "Solve"],
  StringContainsQ[wlText, "First @"] || StringContainsQ[wlText, "First["],
  StringContainsQ[wlText, "Association"] || StringContainsQ[wlText, "<|"],
  StringContainsQ[wlText, "summaryRows"],
  StringContainsQ[wlText, "summaryGrid"],
  StringContainsQ[wlText, "Grid["],
  StringContainsQ[wlText, "checks"]
};
If[! And @@ wlStyleChecks, Print["WL_STYLE_VALIDATION_FAILED"]; Exit[1]];
```

## Boolean Checks and Hard Fail

Every `checks` row must have a single Boolean result. Convert lists and benchmark objects into strict Boolean claims before adding them to `checks`. Wrap symbolic checks as `TrueQ[FullSimplify[claim, Assumptions -> ass]]`; never put raw `And @@ focChecks` or a possible `ConditionalExpression` directly into `checks`.

For self-contained derivations, do not hand-enter a complete final answer table in the check block, such as `expectedCournotEq = Association[...]`, and then compare the derived result to it. That is visually too close to skipping the derivation. Prefer checks that refer back to primitives already defined in the model:

```wolfram
quantityConsistencyClaims = {
  eq["Q"] == Total[eq /@ {"q1", "q2", "q3"}]
};

priceConsistencyClaims = {
  eq["P"] == P[eq["q1"], eq["q2"], eq["q3"]]
};

profitConsistencyClaims = {
  eq["pi1"] == pi1[eq["q1"], eq["q2"], eq["q3"]]
};
```

When the paper itself states target formulas, compare against them only after the model has already been solved, label the block as `paperClaim...`, and comment that the formulas are an external benchmark from the proposition.

For numeric checks, do not write `numericBenchmark == Association["p1" -> ..., ...]` from hand-entered expected values. Use one of these patterns instead:

```wolfram
numericRules = {a -> 10, c1 -> 2, c2 -> 4, gamma -> 1/2};
numericSol = First @ NSolve[focSystem /. numericRules, {p1, p2}, Reals];

numericSolutionCheck = TrueQ[
  Chop[Norm[({p1, p2} /. symbolicSol /. numericRules) - ({p1, p2} /. numericSol)]] == 0
];
```

Or verify numeric residuals directly from the primitives:

```wolfram
numericFOCResidualCheck = TrueQ[
  Chop[Norm[Subtract @@@ (focSystem /. symbolicSol /. numericRules)]] == 0
];
```

Good:

```wolfram
focChecks = FullSimplify[focSystem /. solRules, Assumptions -> $Assumptions];
numericRules = {a -> 10, c1 -> 2, c2 -> 4, gamma -> 1/2};
numericSol = First @ NSolve[focSystem /. numericRules, {p1, p2}, Reals];
numericResidual = Chop[Norm[Subtract @@@ (focSystem /. solRules /. numericRules)]];

checks = {
  {"FOC system holds at selected solution",
   TrueQ[FullSimplify[And @@ focChecks, Assumptions -> $Assumptions]]},
  {"Numeric FOC residual is zero",
   TrueQ[numericResidual == 0]},
  {"Symbolic and numeric prices agree",
   TrueQ[Chop[Norm[({p1, p2} /. solRules /. numericRules) - ({p1, p2} /. numericSol)]] == 0]}
};
```

Bad:

```wolfram
checks = {
  {"FOC system holds", focChecks},              (* list, not Boolean *)
  {"FOC system holds after conjunction", And @@ focChecks}, (* can become ConditionalExpression *)
  {"Numeric benchmark", numericBenchmark},      (* Association, not Boolean *)
  {"Numeric benchmark matches", numericBenchmark == Association["p1" -> 1]} (* hand-entered answer table *)
};
```

Every generated `.wl` must fail the process when checks are false or malformed:

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

If a runtime is available, validate the final file with `scripts/validate_wl_derivation.py`. This catches scripts that merely contain a `checks` variable but never prove that all checks are Boolean `True`. The validator is not the final runtime authority: if it reports `RUNTIME_VALIDATION_SKIPPED`, cannot find Wolfram, or only performs text validation, run the `.wl` directly with the explicit Wolfram executable path and use that command's exit code, stdout success marker, and exported checks CSV as the runtime evidence.

Prefer this explicit runtime check after discovering or receiving the Wolfram executable path:

```powershell
& $wolframExe -script '<absolute-path-to-script.wl>'
```

The task is not complete until that command exits `0` and the generated checks all evaluate to Boolean `True`.

## Economic Formula Transformation Checks

Mathematica is allowed to simplify expressions, but the agent must choose the economically meaningful target form at important steps. `FullSimplify` should verify the transformation; it should not replace the agent's judgment about which form matters for the paper.

Use this pattern whenever a raw derivative, constraint, or ranking needs to be rewritten into an interpretable economic object such as inverse hazard, markup, Lerner index, threshold boundary, envelope condition, or welfare comparison:

```wolfram
(* Raw equation produced directly from primitives. *)
rawEq = D[objective, x] == 0;

(* Target form chosen by economic interpretation, not copied as a final answer. *)
targetEq = lhsTarget == rhsTarget;

(* Pick multiplier only when assumptions imply it is nonzero. *)
multiplierNonzeroCheck =
  TrueQ[FullSimplify[multiplier != 0, Assumptions -> ass]];

rawResidual =
  FullSimplify[multiplier*(Subtract @@ List @@ rawEq), Assumptions -> ass];

targetResidual =
  FullSimplify[multiplier*(Subtract @@ List @@ targetEq), Assumptions -> ass];

transformCheck =
  TrueQ[
    multiplierNonzeroCheck &&
      FullSimplify[rawResidual - targetResidual == 0, Assumptions -> ass]
  ];
```

If the two residuals are negatives of each other, check `rawResidual + targetResidual == 0` instead. Keep `rawResidual`, `targetResidual`, and `transformCheck` visible in the `.wl` script.

### Example 1: Price FOC to inverse-hazard markup

For a monopoly model with demand `1 - F[p/q]` and call cost `callCost[q]`, derive the price FOC from primitives first:

```wolfram
\[Pi]GrossM[p_, q_] := (1 - F[p/q])*(p - callCost[q]);
densityRule = Derivative[1][F][x_] :> f[x];

focPriceRaw =
  D[\[Pi]GrossM[p, q], p] == 0;

focPriceWithf =
  FullSimplify[focPriceRaw /. densityRule, Assumptions -> ass];
```

Then the agent chooses the target economic form:

```wolfram
focPriceTarget =
  (p - callCost[q])/q == (1 - F[p/q])/f[p/q];

priceMultiplierNonzeroCheck =
  TrueQ[FullSimplify[q*f[p/q] != 0, Assumptions -> ass]];

focPriceRawResidual =
  FullSimplify[
    q*(1 - F[p/q]) - (p - callCost[q])*f[p/q],
    Assumptions -> ass
  ];

focPriceTargetResidual =
  FullSimplify[
    q*f[p/q]*(((p - callCost[q])/q) - ((1 - F[p/q])/f[p/q])),
    Assumptions -> ass
  ];

focPriceTransformCheck =
  TrueQ[
    priceMultiplierNonzeroCheck &&
      FullSimplify[
        focPriceRawResidual + focPriceTargetResidual == 0,
        Assumptions -> ass
      ]
  ];
```

This proves the raw FOC and the inverse-hazard markup expression are the same condition under `q > 0` and `f[p/q] > 0`.

### Example 2: Ranking and sign inspection

For threshold or welfare comparisons, do not rely on a bare inequality if the sign structure is hidden. Build the difference and inspect its factored rational form:

```wolfram
rankingDifference =
  FullSimplify[\[CapitalOmega]RPM - \[CapitalOmega]NoRPM,
    Assumptions -> ass];

rankingFactors =
  Factor[Together[rankingDifference]];

rankingCheck =
  TrueQ[
    FullSimplify[
      rankingDifference >= 0,
      Assumptions -> ass
    ]
  ];
```

If `rankingCheck` is not `True`, use `Reduce` to find the exact parameter region:

```wolfram
rankingRegion =
  FullSimplify[
    Reduce[{rankingDifference >= 0, ass}, parameter, Reals],
    Assumptions -> ass
  ];
```

Report the unconditional ranking only when `rankingCheck` is `True`; otherwise report the region returned by `Reduce`.

### Example 3: Threshold boundary from a binding constraint

For a threshold, show the binding equation, all roots, selected root, and feasibility condition before naming the threshold:

```wolfram
constraintBind =
  participationProfit[p] == \[CapitalOmega];

constraintRootsAll =
  FullSimplify[Solve[constraintBind, p, Reals],
    Assumptions -> ass];

constraintRootSelected =
  FullSimplify[p /. constraintRootsAll[[1]], Assumptions -> ass];

thresholdCandidate =
  FullSimplify[
    \[CapitalOmega] /. First @ Solve[
      constraintRootSelected == targetPrice,
      \[CapitalOmega],
      Reals
    ],
    Assumptions -> ass
  ];

thresholdFeasibility =
  FullSimplify[
    Reduce[{constraintBind, feasibilityConstraints, ass},
      {p, \[CapitalOmega]},
      Reals],
    Assumptions -> ass
  ];
```

Only after these objects are visible should the script use a short name such as `OmegaNoRPMM` or `DeltaET`.

## Basic Cell Skeleton

```wolfram
ClearAll["Global`*"];

(* ============================== *)
(* 0. 参数假设 *)
(* ============================== *)

$Assumptions = \[Alpha] > 0 && \[Beta] > 0 &&
   \[Gamma] >= 0 && \[Beta] > \[Gamma];
ass = $Assumptions;
toS[expr_] := ToString[expr, InputForm];

$Assumptions
```

Use Greek letters such as `\[Alpha]`, `\[Beta]`, and `\[Gamma]` whenever they match the source code or paper. In runnable `.wl` scripts, prefer Wolfram escaped Greek symbols over ASCII aliases; escaped forms remain ASCII in the source file while displaying as Greek mathematical objects in Mathematica. Use ASCII aliases only for a documented runtime limitation, and define the mapping immediately.

## Section Order

Use clear separator comments and Chinese economic labels:

```wolfram
(* ============================== *)
(* 1. 模型设定：需求、利润和约束 *)
(* ============================== *)

(* ============================== *)
(* 2. No RPM：经销商零售定价问题 *)
(* ============================== *)

(* step1. 构造经销商利润函数 *)
(* step2. 求一阶条件 FOC *)
(* step3. 求 Hessian / SOC *)
(* step4. 求零售价格反应函数 *)

(* ============================== *)
(* 3. No RPM：合谋价格和外部选择阈值 *)
(* ============================== *)

(* step1. 先写出约束绑定方程 *)
(* step2. 求所有根 *)
(* step3. 选择经济上有效的根 *)
(* step4. 推导非负批发价边界和分区域均衡 *)

(* ============================== *)
(* 4. RPM：竞争、合谋和可行性阈值 *)
(* ============================== *)

(* ============================== *)
(* 5. 阈值排序、数值检验和最终表格 *)
(* ============================== *)
```

For MFN/RPM-style multi-regime models, keep the user's established scenario comments:

```wolfram
(* Stage 1: U chooses w1,w2 *)
(* NoMFN + NoRPM *)
(* MFN + NoRPM *)
(* NoMFN + RPM *)
(* MFN + RPM *)
```

## Source-Notation First Rule

When reproducing an economics model from a paper or Markdown source, the source notation has priority over generic coding convenience. Greek variables must be written as Mathematica Greek symbols so they display as Greek mathematical objects in Mathematica. Use English aliases only when a runtime limitation requires them, and then define the mapping immediately.

Good:

```wolfram
u[\[Theta]_, q_, p_] := \[Theta] q - p
\[Theta]Hat = p/q
demand = 1 - F[\[Theta]Hat]
densityCheck = D[F[\[Theta]], \[Theta]] /. Derivative[1][F][x_] :> f[x]
```

Bad:

```wolfram
u[theta_, q_, p_] := theta*q - p
thetaHat = p/q
demand = 1 - Ffun[thetaHat]
```

For auditable step-by-step scripts, use notebook-style input cells, unsuppressed outputs, or a transcript helper. One acceptable helper is:

```wolfram
show[step_, input_, output_] := (
  Print["===== STEP ", step, " ====="];
  Print["INPUT: ", input];
  Print["OUTPUT: ", InputForm[output]];
  output
);
```

## Naming Rules

Use the user's compact but explicit names:

```wolfram
p2BRNoMFN[w1_, w2_]
piUNoMFNNoRPM[w1_, w2_]
focNoMFNNoRPM
solNoMFNNoRPMAll
solNoMFNNoRPM = First @ solNoMFNNoRPMAll
```

For collusion, deviation, and thresholds:

```wolfram
CollusioninET[w1_, w2_]
FOCcolw1
FOCcolw2
solCollusioninET
WstarinETcoll
MdevinETcoll
DeltaET
OmegaNoRPMM
OmegaNoRPMW0
```

Avoid generic names when a regime-specific name is available. Prefer `pi...`, `foc...`, `sol...All`, `Wstar...`, `Mstar...`, `Collusion...`, `Mdev...`, `Delta...`, and `Omega...`.

## Symbol Discipline

After model primitives are set, do not introduce shortcut symbols like `A`, `B`, `K`, `L`, or `thetaBar` just to make formulas shorter. This often makes the derivation look unlike the user's notebooks and hides economic meaning.

If an abbreviation is unavoidable:

```wolfram
(* B 表示 No RPM 对称零售价中批发价的有效斜率；下面立即检验其展开式 *)
B = 1 + \[Gamma] + \[Gamma] \[Rho];
checkBExpand = FullSimplify[
   B == 1 + \[Gamma] + \[Gamma] \[Rho],
   Assumptions -> $Assumptions
];
```

Prefer writing the expanded expression in final outputs unless the paper itself defines the abbreviation.

## Regime Result Associations

At the end of each regime, collect all economically relevant objects into an `Association`:

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

discEq
```

Use the same key order across regimes:

```wolfram
{"w1", "w2", "p1", "p2", "q1", "q2", "piU", "pi2", "pi1"}
```

If a regime makes a profit mechanically zero, write `"pi1" -> 0` or `"pi2" -> 0` directly.

## Final Output List and Grid

For multi-regime comparison, use a final WL-facing grid:

```wolfram
summaryRows4 = {
  {"批发价 (w_1)", discEq["w1"], mfnEq["w1"], discRPMEq["w1"], mfnRPMEq["w1"]},
  {"批发价 (w_2)", discEq["w2"], mfnEq["w2"], discRPMEq["w2"], mfnRPMEq["w2"]},
  {"零售价 (p_1)", discEq["p1"], mfnEq["p1"], discRPMEq["p1"], mfnRPMEq["p1"]},
  {"零售价 (p_2)", discEq["p2"], mfnEq["p2"], discRPMEq["p2"], mfnRPMEq["p2"]},
  {"销量 (q_1)", discEq["q1"], mfnEq["q1"], discRPMEq["q1"], mfnRPMEq["q1"]},
  {"销量 (q_2)", discEq["q2"], mfnEq["q2"], discRPMEq["q2"], mfnRPMEq["q2"]},
  {"上游利润 (pi_U)", discEq["piU"], mfnEq["piU"], discRPMEq["piU"], mfnRPMEq["piU"]},
  {"经销商利润 (pi_2)", discEq["pi2"], mfnEq["pi2"], discRPMEq["pi2"], mfnRPMEq["pi2"]},
  {"经销商利润 (pi_1)", discEq["pi1"], mfnEq["pi1"], discRPMEq["pi1"], mfnRPMEq["pi1"]}
};

summaryGrid4 = Grid[
  Prepend[summaryRows4, {"对象", "NoMFN+NoRPM", "MFN+NoRPM", "NoMFN+RPM", "MFN+RPM"}],
  Frame -> All,
  ItemStyle -> Directive[14],
  Alignment -> {Left, Center, Center, Center, Center}
];

summaryGrid4
```

For threshold propositions, use:

```wolfram
thresholdRows = {
  {"No RPM 诱导垄断价格阈值", OmegaNoRPMM},
  {"No RPM 非负批发价可行边界", OmegaNoRPMW0},
  {"RPM 诱导垄断价格阈值", OmegaRPMM}
};

thresholdGrid = Grid[
  Prepend[thresholdRows, {"对象", "表达式"}],
  Frame -> All,
  ItemStyle -> Directive[14],
  Alignment -> {Left, Center}
];

thresholdGrid
```

## Full Threshold Derivation Requirement

Do not jump directly to a threshold formula. Show the whole chain:

```wolfram
constraintBindNoRPM = piDealerNoRPM[p] == \[CapitalOmega];
solConstraintBindNoRPMAll = FullSimplify[
   Solve[constraintBindNoRPM, p, Reals],
   Assumptions -> $Assumptions
];

pNoRPMCol = FullSimplify[
   p /. solConstraintBindNoRPMAll[[1]],
   Assumptions -> $Assumptions
];

wNoRPMCol = FullSimplify[
   wNoRPMFromP[pNoRPMCol],
   Assumptions -> $Assumptions
];

OmegaNoRPMW0 = FullSimplify[
   \[CapitalOmega] /. First @ Solve[wNoRPMCol == 0, \[CapitalOmega], Reals],
   Assumptions -> $Assumptions
];

regionNoRPMCanInduceM = FullSimplify[
   0 <= \[CapitalOmega] <= OmegaNoRPMM,
   Assumptions -> $Assumptions
];
```

For each region, solve or state the equilibrium object inside that region, not only the boundary:

```wolfram
NoRPMRegionI = Association[
  "condition" -> 0 <= \[CapitalOmega] <= OmegaNoRPMM,
  "p" -> pM,
  "w" -> wNoRPMInduceM
];

NoRPMRegionII = Association[
  "condition" -> OmegaNoRPMM < \[CapitalOmega] <= OmegaNoRPMW0,
  "p" -> pNoRPMCol,
  "w" -> wNoRPMCol
];
```

## Commands to Prefer

- FOC: `D[profit, var] == 0`
- Solve closed-form systems: `Solve[eqs, vars, Reals]//Simplify`
- Strong simplification: `FullSimplify[expr, Assumptions -> $Assumptions]`
- Hessian/SOC: `D[profit, {{vars}, 2}]`, `Eigenvalues[...]`, `NegativeDefiniteMatrixQ[...]` where useful
- Feasible region: `Reduce[{constraints}, vars, Reals]`
- Ranking proof: `FullSimplify[OmegaNoRPMM < OmegaRPMM, Assumptions -> $Assumptions]`
- Sign inspection: `Factor[Together[OmegaRPMM - OmegaNoRPMM]]`
- Numeric sanity check: `N[expr /. {\[Gamma] -> 1, \[Rho] -> 1, \[CapitalOmega] -> 0.06}, 16]`

## Verification Rows

Every serious replication should include checks, but checks are not the main user-facing output:

```wolfram
checks = {
   {"FOC 解与声明的反应函数一致",
    FullSimplify[p2BRNoMFN[w1, w2] == claimedP2BR, Assumptions -> $Assumptions]},
   {"Hessian 满足二阶条件",
    FullSimplify[And @@ Thread[Eigenvalues[hessianDealer] < 0], Assumptions -> $Assumptions]},
   {"阈值排序成立",
    FullSimplify[OmegaNoRPMM <= OmegaNoRPMW0 <= OmegaRPMM, Assumptions -> $Assumptions]}
};

checkRows = Join[
   {{"Check", "Result"}},
   ({#[[1]], toS[#[[2]]]} & /@ checks)
];
```

Export `checkRows` to CSV after the `.wl` derivation is complete.
