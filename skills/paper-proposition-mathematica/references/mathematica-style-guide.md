# Mathematica Style Guide for Paper Proposition Replication

This guide captures a reusable Mathematica workflow for economics/game-theory paper derivations. The priority is a human-readable `.wl` derivation script that looks close to the user's provided style examples: ordered economic sections, explicit intermediate objects, visible symbolic outputs, `Association`, and final `Grid` summaries. A `.nb` is optional and should be generated only when the user asks for it.

## Style-Exemplar WL Protocol

For the user's model derivation tasks:

1. Inspect representative style-exemplar files when available. If the user gives a folder, sample several `.wl`, `.m`, and `.nb` files, prioritizing files whose names or contents match the current model family.
2. Run Mathematica step by step with small kernel inputs while deriving. Do not treat a single final script run as the whole derivation process.
3. Assemble a complete `.wl` script after the derivation is clear. The `.wl` is the main artifact.
4. Keep the output of each economic step visible in the `.wl` style: FOC, solution list, selected solution, threshold equation, threshold roots, feasible region, `Association`, and final `Grid`.
5. Export CSV/check tables only as verification artifacts. Generate `.nb` only when explicitly requested.

If no user-provided style exemplar is available, use the bundled default example `examples/mfn-rpm-nonash-competition-style.wl`. It is a runnable conditional-stationary-point style example, not a proof of full equilibrium over its declared parameter domain. Preserve the format without importing its economic assumptions.

When stepwise input is piped through `wolfram.exe -noprompt`, set the output folder explicitly because `$InputFileName` is empty. On Windows, direct `wolfram.exe -script` can be unreliable for raw Chinese strings in UTF-8 `.wl` files; if this happens, keep the `.wl` ASCII-only or encode Chinese labels with Wolfram escapes / `FromCharacterCode`.

## WL Script Must Match the Style Exemplar

The `.wl` is the main deliverable unless the user explicitly asks for `.nb`. Do not produce a compact batch exporter as the main script. The script should read like the user's provided Mathematica/WL examples:

- begin with `ClearAll["Global`*"];`;
- define `$Assumptions` early;
- use section comments and step comments;
- define functions with patterns, e.g. `piUDisc[w1_, w2_] := ...`;
- derive FOCs explicitly, e.g. `focDisc = {...}`;
- solve full systems, e.g. `solDiscW = FullSimplify[Solve[focDisc, {w1, w2}], Assumptions -> $Assumptions]`;
- retain all candidates and conditions, then select rules with a mathematical/economic rationale; `First` is allowed but not required;
- collect regime results into `discEq`, `mfnEq`, `discRPMEq`, `mfnRPMEq`, or analogous `Association` objects;
- build `summaryRows` and `summaryGrid = Grid[...]`;
- put `summaryGrid` on its own final line without a semicolon;
- leave key objects unsuppressed, matching the notebook code style.

The bundled default example uses this same pattern. In particular, copy its high-level structure rather than its economic content: assumptions, primitives, one block per regime, FOC solving, `Association` result objects, and final `summaryGrid`.

The following optional style heuristic is for full multi-regime deliverables. Tokens do not establish mathematical correctness, and a focused derivation need not contain every one:

```wolfram
wlText = Import[wlPath, "Text"];
wlStyleChecks = {
  StringContainsQ[wlText, "ClearAll[\"Global`*\"]"],
  StringContainsQ[wlText, "$Assumptions"],
  StringContainsQ[wlText, "FullSimplify"],
  StringContainsQ[wlText, "Solve"],
  StringContainsQ[wlText, "Association"] || StringContainsQ[wlText, "<|"],
  StringContainsQ[wlText, "summaryRows"],
  StringContainsQ[wlText, "summaryGrid"],
  StringContainsQ[wlText, "Grid["],
  StringContainsQ[wlText, "checks"]
};
If[! And @@ wlStyleChecks, Print["WL_STYLE_ADVISORY"]];
```

## Technical Checks, Mathematical Evidence and Completion

Keep three distinct records: executable technical assertions; raw mathematical claims/results with assumptions, quantifiers and proof status; acceptance of the user's requested scope. Every technical `checks` row must be `{nonblank string, True|False}` and the list must be nonempty. Preserve raw symbolic expressions before applying `TrueQ`; False from `TrueQ` is not automatically a counterexample or proof of negation. A timeout or an unevaluated `Reduce` remains unresolved.

Derive from primitives before comparing paper formulas or expected values. Benchmarks need a traceable source and independent purpose; their variable names do not determine validity. For example, compare the derived quantity to `Total[eq /@ {"q1", "q2", "q3"}]`, price to `P[eq["q1"], eq["q2"], eq["q3"]]`, and profit to `pi1[eq["q1"], eq["q2"], eq["q3"]]`, using the original definitions. Such consistency checks do not by themselves establish optimality.

Construct residuals before substitution, because an equation can evaluate to True/False and lose its two sides:

```wolfram
focResiduals = {D[(x - 1)^2, x]};
focSystem = Thread[focResiduals == ConstantArray[0, Length[focResiduals]]];
solAll = Solve[focSystem, {x}, Reals];
(* This example is a linear FOC with one real root; no optimality claim. *)
If[Length[solAll] != 1, Print["UNRESOLVED_SELECTION"]; Exit[1]];
sol = First[solAll];
rawFOCResidual = FullSimplify[focResiduals /. sol];
checks = {{"Candidate satisfies primitive FOC", TrueQ[rawFOCResidual == {0}]}};
```

If previously stored equations have already become Boolean, reconstruct residuals from the primitive objective. Do not apply `Subtract` to Boolean values. For requested numeric work use `N[focResiduals /. symbolicSol /. numericRules, precision]` with a justified tolerance. Compare symbolic and numeric solutions on the same branch and domain, retaining `NSolve`'s full root set. `FindRoot` establishes only the root found, not uniqueness or completeness. Numerical residuals do not replace an exact proof.

Use the following technical guard (or equivalent) before reporting registered checks as passing:

```wolfram
If[!ListQ[checks] || Length[checks] == 0 ||
   !AllTrue[checks, MatchQ[#, {_String, _}] &&
     StringLength[StringTrim[First[#]]] > 0 &],
   Print["CHECKS_EMPTY_OR_MALFORMED"]; Exit[1]
];
checkResults = Last /@ checks;
If[!VectorQ[checkResults, BooleanQ] || !TrueQ[And @@ checkResults],
   Print["CHECKS_FAILED_OR_MALFORMED"]; Print[InputForm[checks]]; Exit[1]
];
```

Run the completed script once through `scripts/validate_wl_derivation.py` with the discovered executable, explicit task-specific work directory and appropriate timeout. The command in the parent SKILL shows the invocation with user-selected paths. The validator distinguishes advisory style, explicit static-only inspection, absent runtime, execution failure, timeout, missing/empty/malformed checks, non-Boolean/false results and missing completion. It requires its own current-run marker, not a marker printed by the target. Do not end a normally completing target with `Exit[0]`, which prevents the wrapper from completing. A passing run verifies only its registered checks, not the full model. Manual direct runs need equivalent completion evidence; do not run an expensive script twice merely to count checks.

A valid refutation can complete an audit. A conditional solution can complete a conditional-solution task with its domain and limits. An unresolved claim required for the requested positive proof remains incomplete, even when technical checks pass. Keep scope/status evidence separate from the process result.

## Economic Formula Transformation Checks

Mathematica is allowed to simplify expressions, but the agent must choose the economically meaningful target form at important steps. `FullSimplify` should verify the transformation; it should not replace the agent's judgment about which form matters for the paper.

At each important rewrite distinguish an identity, equivalence of solution sets, and a one-way implication. Build residuals directly from the primitive expressions, before equations evaluate:

```wolfram
rawResidual = D[objective, x];
targetResidual = lhsTarget - rhsTarget;
rawEq = rawResidual == 0;
targetEq = targetResidual == 0;

(* One valid method: a proved nonzero proportional factor, on originalDomain. *)
rawFactorEvidence = FullSimplify[factor != 0, Assumptions -> originalDomain];
rawIdentityEvidence = FullSimplify[
  rawResidual == factor targetResidual, Assumptions -> originalDomain];
transformCheck = TrueQ[rawFactorEvidence] && TrueQ[rawIdentityEvidence];
```

Here `factor` is derived and justified, not guessed. Preserve `originalDomain`, including denominators and real/complex choices. Check nonempty feasibility or explicitly retain unknown nonemptiness; otherwise a vacuous implication can masquerade as a result. An alternative is `Resolve`/`Reduce` for logical equivalence on a specified domain. Do not require literally equal residuals: `2 x == 0` and `x == 0` are equivalent. Conversely, cancelling `a` in `a x == 0` loses the `a == 0` branch unless a nonzero condition is proved. Squaring and inequalities require their own branch/sign conditions. If only one implication is proved, state its direction. Large problems can use justified factorization and domain splits instead of one high-dimensional reduction.

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

rawPriceMultiplierEvidence = FullSimplify[q*f[p/q] != 0, Assumptions -> ass];
priceMultiplierNonzeroCheck = TrueQ[rawPriceMultiplierEvidence];

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

rawRankingEvidence = FullSimplify[
  rankingDifference >= 0, Assumptions -> ass];
rankingCheck = TrueQ[rawRankingEvidence];
```

If `rankingCheck` is not `True`, use `Reduce` to find the exact parameter region:

```wolfram
rankingRegion =
  FullSimplify[
    Reduce[{rankingDifference >= 0, ass}, parameter, Reals],
    Assumptions -> ass
  ];
```

Preserve the raw simplification before `TrueQ`. Report a ranking only on the proved original domain; if `Reduce` returns unresolved or conditional output, retain that output and status rather than treating it as a solved region. Do not call a ranking unconditional when it relies on parameter assumptions.

### Example 3: Threshold boundary from a binding constraint

For a threshold, retain the binding equation, all roots and their validity conditions. A complete feasible relation can be preferable to premature root selection:

```wolfram
constraintResidual = participationProfit[p] - \[CapitalOmega];
constraintBind = constraintResidual == 0;
constraintRootsAll = Solve[constraintBind, p, Reals];
thresholdFeasibility = Reduce[
  constraintBind && feasibilityConstraints && ass,
  {p, \[CapitalOmega]}, Reals];
thresholdRelation = Reduce[
  constraintBind && p == targetPrice && feasibilityConstraints && ass,
  {p, \[CapitalOmega]}, Reals];
```

Here feasibility and target price must come from the original model. Inspect whether relations were solved; keep unresolved branches. Select a scalar threshold only after justifying which branch applies, recording any degeneracy and excluded cases. A single generic `Solve` rule is not proof of uniqueness at exceptional parameters. No automatic `[[1]]`/`First` selection is required.

## Basic Cell Skeleton

The following parameter domain is illustrative only; replace it with the original model domain. Do not import these restrictions into a different model.

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

Use clear separator comments and labels in the user's preferred language; this example uses Chinese:

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
(* Only after validating singleton structure, parameter conditions and selection rationale. *)
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

Do not jump directly to a threshold formula. Show the binding condition, candidate family and all relevant feasible boundaries:

```wolfram
constraintBindNoRPM = piDealerNoRPM[p] == \[CapitalOmega];
solConstraintBindNoRPMAll = Solve[constraintBindNoRPM, p, Reals];
regionConstraintNoRPM = Reduce[
  constraintBindNoRPM && feasibilityConstraints && $Assumptions,
  {p, \[CapitalOmega]}, Reals];
regionNoRPMW0 = Reduce[
  constraintBindNoRPM && wNoRPMFromP[p] == 0 &&
    feasibilityConstraints && $Assumptions,
  {p, \[CapitalOmega]}, Reals];
```

After resolving branches, store the selected `pNoRPMCol`, its domain, `wNoRPMCol = wNoRPMFromP[pNoRPMCol]`, and the justified scalar threshold `OmegaNoRPMW0`. If selection or a boundary remains unresolved, keep the complete relation and label it accordingly. Do not invent a scalar answer to populate a table. The region table below illustrates a model-specific arrangement; derive its ordering and solution validity before using it.

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

Preserve raw evidence before building the strict Boolean technical table. These are illustrative claim forms; only include the relevant justified claims for the model and task:

```wolfram
rawFormulaEvidence = FullSimplify[
  p2BRNoMFN[w1, w2] == claimedP2BR, Assumptions -> $Assumptions];
rawSOCEvidence = FullSimplify[
  And @@ Thread[Eigenvalues[hessianDealer] < 0], Assumptions -> $Assumptions];
rawRankingEvidence = FullSimplify[
  OmegaNoRPMM <= OmegaNoRPMW0 <= OmegaRPMM, Assumptions -> $Assumptions];
checks = {
  {"Displayed formulas agree", TrueQ[rawFormulaEvidence]},
  {"Strict interior Hessian criterion holds", TrueQ[rawSOCEvidence]},
  {"Threshold ordering holds on stated domain", TrueQ[rawRankingEvidence]}
};
checkRows = Join[{{"Check", "Result"}},
  ({#[[1]], toS[#[[2]]]} & /@ checks)];
```

A False technical assertion requires investigation; distinguish an incorrect claim from unresolved evidence. A zero Hessian need not exclude a maximum, and a boundary maximum need not satisfy an interior FOC. Choose the appropriate argument. Export checks after the stepwise derivation, retaining all mathematical evidence and stated proof boundaries.
