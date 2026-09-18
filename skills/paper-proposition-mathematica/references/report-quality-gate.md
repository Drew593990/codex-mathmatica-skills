# Mathematical Report Quality Gate

Use for mathematical derivation reports and revisions, independent of the
chosen solver. Keep the existing model, notation, user-approved scope, and
output location. Do not add numerical exercises, agents, approvals, or a new
environment just to perform this gate.

## 1. Establish the contract before drafting

Record the following in the existing project specification or a short report
contract. For a narrow correction, extend the existing inventory rather than
creating a new reporting system.

- Symbol map: general variables, conditional responses, named solutions,
  evaluation points, superscripts/subscripts, and first-use definitions.
- Required scenarios and result items, derived from the user's request/model,
  not reconstructed from whichever exports happen to exist.
- For each item: explicit / conditional / unsolved / not applicable, the reason
  for missing or inapplicable results, and its defining/validity conditions.
- Required locations: each relevant derivation's final expressions and nearby
  result/condition tables; include requested appendix material separately.

Use the project's own conventions. M and S below are examples, not universal
requirements. For a single optimization problem, preserve its star/hat/index.

Formula representation status and proof status are separate. Preserve the statement, assumptions, quantifiers, requested proof level and unresolved scope when handing results to the writer; conclusions must not be stronger than the derivation.

## 2. Separate expressions from evaluated results

Compute derivatives in general coordinates first. Use structured symbol or AST
substitution to construct named result objects, then export their TeX. Do not
rename by global string replacement. Treat q_M as a symbol during algebraic
substitution and as q_M(r) when taking an equilibrium total derivative.

| Object | Example | Required distinction |
|---|---|---|
| General function | P(q,x), H(q,x;r) | Variables are not equilibrium values |
| Conditional response | x(q;r), x_S(q) | Quality remains given |
| Market result | q_M(r), x_M(r) | Market evaluation context |
| Social result | q_S, x_S=x_S(q_S) | Social evaluation context |
| Evaluated derivative | P_q(q_M,x_M) | Differentiate first, then evaluate |
| Total derivative | dP(q_M(r),x_M(r))/dr | Include every varying argument |
| Optimization alternatives | max over q,x | Do not add equilibrium subscripts |

For a long formula, explicit arguments or a precisely defined evaluation bar
are acceptable. A distant sentence saying "everything is at equilibrium" is
not enough for final boxed results with otherwise ambiguous bare variables.
Apply this to comparative statics, inequalities, parameter examples, captions,
and conclusions, not only prices and profits in tables.

Each new quantity must be defined before its first substantive use: meaning,
units if relevant, differentiation path/held-fixed variables, and domain.
For example, define a pass-through rate by the price derivative before giving
its Hessian-based calculation formula. Do not treat a derived representation
as a substitute for the definition.

## 3. Generate body and tables from the same named objects

Use one canonical result catalog for body equations, result tables, condition
tables, and repeated final formulas. Keep algebraic identities/general
derivations distinct from named outcomes. Export free-symbol information from
the symbolic objects before converting to strings.

If an existing report is handwritten, inventory its final expressions and
compare them with the independently derived named objects. Migrate affected
repeated formulas incrementally; do not rewrite unrelated chapters for tooling.
Never obtain the "canonical" formula by scraping the report being tested.

Use exact symbolic checks after substitution, with real model assumptions and
without assuming the desired conclusion. A reversible renaming check and an
objective/FOC residual check have different purposes; keep them separate.
Do not use solver output failure as a proof that a closed form cannot exist.

## 4. Four acceptance gates

1. Mathematical: identities, derivative paths, domain/regime, conditional versus
   solved status, and the actual optimality/equilibrium claim. Preserve unknowns.
2. Notation/content: inspect every final expression and its preceding prose;
   check both sides of equations, powers, indexes, evaluation points, and
   first-use definitions. Inspect all registered occurrences and scan the rest
   of the document for unregistered final formulas.
3. Coverage: every required scenario/item appears in the relevant result table;
   conditions are separately available. A threshold or FOC table cannot replace
   the price/quantity/profit/welfare results. Pending results remain listed.
4. Rendered output: compile, inspect changed pages and affected page breaks,
   tables, references and equations. For a new/full report, inspect all pages.

Record evidence, actual findings, unresolved items, and final artifact hashes
in the project. Never fill a checklist with "passed" from memory or solely
because a tool exited zero. Any relevant change invalidates the corresponding
checks; recheck affected content before claiming readiness. The main agent
remains responsible, whether or not a reviewer agent is available.

Read the final report once in reader order: each symbol must be understandable
at the point of use, every result must have its determination/status nearby,
and the final expressions must agree with the computed objects. This is not a
second round of rewriting the mathematics from memory.

An unresolved claim required for a positive proof prevents accepting that proof. A verified refutation can complete an audit; a complete conditional derivation can be accepted within its declared scope while disclosing that global optimality or SPE is outside that scope. Keep required pending items in the inventory. Pure theory does not require statistical power, simulation or external citations for every original derivation step. Writing evaluation and simulated peer review are not independent mathematical proofs.

## 5. Revision sweep

After a corrected symbol, definition, condition, or outcome, search its full
family of occurrences: body, results, conditions, examples, captions, summary,
appendix, and generator sources. Do not fix only the highlighted PDF region.
Do not add a new correct appendix while leaving the old main derivation intact.

For explanation-only requests, answer without changing files. Once the user
requests correction, apply the scoped correction and the same-family sweep
without asking again for approval already granted.

## 6. Mechanical contract checker

Run `scripts/validate_report_contract.py` for structured export/report flows:

```powershell
python '<skill-directory>/paper-proposition-mathematica/scripts/validate_report_contract.py' '<project>/report-contract.json' --root '<project>' --output '<project>/report-contract-check.json'
```

The UTF-8 JSON contract contains:

- `version`: 1.
- `catalog`: `file` (project-relative JSON) and its `sha256`, captured from the
  named symbolic export. The hash detects stale inputs, not mathematical truth.
- `contexts`: name to `forbidden_free_symbols` list. For example, the market
  context can forbid `q,x`, while a generic-derivative context allows them.
- `requirements`: scenario/item rows with `formula` ID, required `placements`
  (must include `result_table`), and a list of `conditions` formula IDs. Empty
  conditions are allowed only for explicitly unsolved/inapplicable items.
- `files`: every relevant report source file relative to the project root.
- `occurrences`: formula ID, file, unique `begin` and `end` marker strings, and
  placement (`body`, `result_table`, `condition_table`, `caption`, `conclusion`).
  Markers enclose exactly the exported expression, excluding math delimiters
  and labels. Use unique TeX comments on separate lines for normal TeX projects.
- `definitions`: symbol, file, unique `definition` and `first_use` anchors, in
  reading order. For definitions spanning files, use an expanded read-order
  text generated from the actual report or record a manual cross-file check;
  the script only compares order within one inventoried file.

The catalog maps IDs to `tex`, `context`, `free_symbols`, and `status`.
Status is `explicit`, `conditional`, `unsolved`, `not_applicable`, `condition`,
or `identity`; unsolved/inapplicable items also require an `explanation`.
Optional `proof_status` (`proved`, `refuted`, `unresolved`) and `proof_evidence` may accompany a catalog entry as explanatory metadata. They do not replace the version-1 `status` enum or existing requirements. The current checker neither validates these optional fields nor authenticates their truth; review evidence separately.
Examples and all regression fixtures are in `scripts/test_report_contract.py`.

The checker compares registered report text with canonical text, checks the
required placements/conditions, notices forbidden exported free symbols, and
checks registered definition ordering. It intentionally preserves separating
spaces in TeX commands. Formatting changes must be regenerated from the source
or checked for equivalence; do not weaken a mismatch into a silent pass.

**Limits:** it does not parse arbitrary TeX mathematically, prove the catalog,
discover every omitted scenario, validate claimed solution status, infer all
unregistered symbol uses, or inspect PDF rendering. A fabricated contract or
symbol inventory can defeat it. Use real symbolic exports and a requirements
inventory independent of the generated tables; manually review the remaining
coverage and semantics. Its success is not full report acceptance.

When introducing a new generator/checker, deliberately test: omitted body
subscript with a correct table, omitted superscript, missing scenario/item,
missing result table, missing conditions, stale formulas, definition after use,
and a valid generic derivative that must NOT receive equilibrium subscripts.
Do not claim autonomous model compliance has been demonstrated by unit tests.
