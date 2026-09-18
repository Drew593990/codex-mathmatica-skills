ClearAll["Global`*"];
$Assumptions = True;
focResiduals = {D[(x - 1)^2, x]};
solAll = Solve[Thread[focResiduals == {0}], {x}, Reals];
If[Length[solAll] != 1, Print["SELECTION_FAILED"]; Exit[1]];
selected = First[solAll];
rawUnknown = FullSimplify[x > 0, Assumptions -> Element[x, Reals]];
checks = {
  {"residual formed before substitution", TrueQ[(focResiduals /. selected) == {0}]},
  {"proportional equations are equivalent",
    TrueQ[Resolve[ForAll[x, Equivalent[2 x == 0, x == 0]], Reals]]},
  {"unrestricted cancellation loses a branch",
    TrueQ[Resolve[Exists[{a, x}, a x == 0 && x != 0], Reals]]},
  {"nonzero condition restores equivalence",
    TrueQ[Resolve[ForAll[{a, x}, Implies[a != 0,
      Equivalent[a x == 0, x == 0]]], Reals]]},
  {"flat Hessian can coexist with global maximum",
    TrueQ[(D[-x^4, {x, 2}] /. x -> 0) == 0 &&
      Resolve[ForAll[x, -x^4 <= 0], Reals]]},
  {"boundary maximum need not satisfy interior FOC",
    TrueQ[D[-x, x] != 0 &&
      Resolve[ForAll[x, Implies[x >= 0, -x <= 0]], Reals]]},
  {"open interval has no maximizing point",
    TrueQ[Resolve[ForAll[x, Implies[0 < x < 1,
      Exists[y, x < y < 1]]], Reals]]},
  {"vacuous implication does not establish a feasible domain",
    TrueQ[Reduce[a > 0 && a < 0, a, Reals] === False &&
      Resolve[ForAll[a, Implies[a > 0 && a < 0, a == 1]], Reals]]},
  {"both algebraic roots retained",
    TrueQ[Sort[x /. Solve[x^2 == 1, x, Reals]] == {-1, 1}]},
  {"unknown not automatically a refutation",
    TrueQ[!BooleanQ[rawUnknown] && !TrueQ[rawUnknown]]},
  {"one pass simultaneous symbol substitution",
    TrueQ[Expand[(x + 2 y) /. {x -> y, y -> x}] == 2 x + y]}
};
If[!ListQ[checks] || Length[checks] == 0 ||
   !AllTrue[checks, MatchQ[#, {_String, _}] &&
     StringLength[StringTrim[First[#]]] > 0 &], Exit[1]];
If[!VectorQ[Last /@ checks, BooleanQ] ||
   !TrueQ[And @@ (Last /@ checks)], Print[checks]; Exit[1]];
Print["SEMANTICS_CHECKS_OK"];
