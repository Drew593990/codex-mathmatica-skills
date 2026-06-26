(* ::Package:: *)

(* ::Input:: *)
(* ::Section::*)(*Basic Model with Cross-Price Effects (alpha),4 cases (NO Nash Bargaining) Demand:q1=1-p1+\[Alpha] p2 q2=a-p2+\[Alpha] p1 Market 1 competition constraint:p1=w1 Cases:1) NoMFN+NoRPM 2) MFN+NoRPM 3) NoMFN+RPM 4) MFN+RPM*)


(* ::Input:: *)
ClearAll["Global`*"];


(* ::Input:: *)
(*-----------------------0. Assumptions-----------------------*)


(* ::Input:: *)
$Assumptions=a>1&&c\[Element]Reals&&-1<\[Alpha]<1;


(* ::Input:: *)
(*-----------------------1. Demand and Profits-----------------------*)


(* ::Input:: *)
q1[p1_,p2_]:=1-p1+\[Alpha] p2;
q2[p2_,p1_]:=a-p2+\[Alpha] p1;

(*profits*)
piU[w1_,w2_,p1_,p2_]:=(w1-c) q1[p1,p2]+(w2-c) q2[p2,p1];
pi1[p1_,w1_,p2_]:=(p1-w1) q1[p1,p2];
pi2[p2_,w2_,p1_]:=(p2-w2) q2[p2,p1];

(*Market 1 constraint*)
p1FromW1[w1_]:=w1;


(* ::Input:: *)
(*-----------------------2. Case 1:NoMFN+NoRPM-----------------------*)
(*Stage 2:D2 chooses p2 given (w1,w2) and p1=w1*)


(* ::Input:: *)
p2BR[w1_,w2_]=FullSimplify[p2/. First@Solve[D[pi2[p2,w2,p1FromW1[w1]],p2]==0,p2],Assumptions->$Assumptions]


(* ::Input:: *)
(*Verify: raw FOC residual and best-response target residual are equivalent*)
p2BRRawFOCResidual=FullSimplify[D[pi2[p2,w2,p1FromW1[w1]],p2],Assumptions->$Assumptions];
p2BRTargetResidual=FullSimplify[2 p2-(a+\[Alpha] w1+w2),Assumptions->$Assumptions];
p2BRMultiplierNonzeroCheck=TrueQ[FullSimplify[2!=0,Assumptions->$Assumptions]];
p2BRTransformCheck=TrueQ[p2BRMultiplierNonzeroCheck&&FullSimplify[p2BRRawFOCResidual+p2BRTargetResidual==0,Assumptions->$Assumptions]]




(* ::Input:: *)



(* ::Input:: *)
p2BRNoMFN[w1_,w2_]=p2BR[w1,w2]



(* ::Input:: *)

(*Stage 1:U chooses w1,w2*)
piUNoMFNNoRPM[w1_,w2_]=FullSimplify[piU[w1,w2,p1FromW1[w1],p2BRNoMFN[w1,w2]],Assumptions->$Assumptions]



(* ::Input:: *)



(* ::Input:: *)

focNoMFNNoRPM={D[piUNoMFNNoRPM[w1,w2],w1]==0,D[piUNoMFNNoRPM[w1,w2],w2]==0};

solNoMFNNoRPMAll=FullSimplify[Solve[focNoMFNNoRPM,{w1,w2}],Assumptions->$Assumptions];
solNoMFNNoRPM=First@solNoMFNNoRPMAll



(* ::Input:: *)



(* ::Input:: *)


discEq=<|"w1"->FullSimplify[w1/. solNoMFNNoRPM,Assumptions->$Assumptions],"w2"->FullSimplify[w2/. solNoMFNNoRPM,Assumptions->$Assumptions],"p1"->FullSimplify[p1FromW1[w1]/. solNoMFNNoRPM,Assumptions->$Assumptions],"p2"->FullSimplify[p2BRNoMFN[w1,w2]/. solNoMFNNoRPM,Assumptions->$Assumptions],"q1"->FullSimplify[q1[p1FromW1[w1],p2BRNoMFN[w1,w2]]/. solNoMFNNoRPM,Assumptions->$Assumptions],"q2"->FullSimplify[q2[p2BRNoMFN[w1,w2],p1FromW1[w1]]/. solNoMFNNoRPM,Assumptions->$Assumptions],"piU"->FullSimplify[piUNoMFNNoRPM[w1,w2]/. solNoMFNNoRPM,Assumptions->$Assumptions],"pi2"->FullSimplify[pi2[p2BRNoMFN[w1,w2],w2,p1FromW1[w1]]/. solNoMFNNoRPM,Assumptions->$Assumptions],"pi1"->0|>






(* ::Input:: *)



(* ::Input:: *)




(*-----------------------3. Case 2:MFN+NoRPM-----------------------*)
(*MFN=>w1=w2=w;p1=w;D2 chooses p2*)


(* ::Input:: *)
p2BRMFN[w_]:=FullSimplify[p2BR[w,w],Assumptions->$Assumptions];



(* ::Input:: *)

piUMFNNoRPM[w_]:=FullSimplify[piU[w,w,w,p2BRMFN[w]],Assumptions->$Assumptions];



(* ::Input:: *)
focMFNNoRPM=FullSimplify[D[piUMFNNoRPM[w],w]==0,Assumptions->$Assumptions];
solMFNNoRPMAll=FullSimplify[Solve[focMFNNoRPM,w],Assumptions->$Assumptions];
solMFNNoRPM=First@solMFNNoRPMAll



(* ::Input:: *)



(* ::Input:: *)


mfnEq=<|"w1"->FullSimplify[w/. solMFNNoRPM,Assumptions->$Assumptions],"w2"->FullSimplify[w/. solMFNNoRPM,Assumptions->$Assumptions],"p1"->FullSimplify[w/. solMFNNoRPM,Assumptions->$Assumptions],"p2"->FullSimplify[p2BRMFN[w]/. solMFNNoRPM,Assumptions->$Assumptions],"q1"->FullSimplify[q1[w,p2BRMFN[w]]/. solMFNNoRPM,Assumptions->$Assumptions],"q2"->FullSimplify[q2[p2BRMFN[w],w]/. solMFNNoRPM,Assumptions->$Assumptions],"piU"->FullSimplify[piUMFNNoRPM[w]/. solMFNNoRPM,Assumptions->$Assumptions],"pi2"->FullSimplify[pi2[p2BRMFN[w],w,w]/. solMFNNoRPM,Assumptions->$Assumptions],"pi1"->0|>




(* ::Input:: *)



(* ::Input:: *)



(* ::Input:: *)
(*-----------------------4. Case 3:NoMFN+RPM-----------------------*)
(*RPM:U sets retail p2 in market 2. With linear wholesale contract and D2 participation,w2 does not affect demand,so optimal sets w2=p2 (binding PC) to extract margin;then pi2=0.*)

(*test sign*)


(* ::Input:: *)
 solpiUp2 =D[piU[w1,w2,p1,p2],p2]//FullSimplify



(* ::Input:: *)
(*binding PC*)




(* ::Input:: *)
Collect[solpiUp2,c]


(* ::Input:: *)
w2FromP2RPM[p2_]:=p2;

piUNoMFNRPM[w1_,p2_]:=FullSimplify[piU[w1,w2FromP2RPM[p2],p1FromW1[w1],p2],Assumptions->$Assumptions];


(* ::Input:: *)
focNoMFNRPM={D[piUNoMFNRPM[w1,p2],w1]==0,D[piUNoMFNRPM[w1,p2],p2]==0};

solNoMFNRPMAll=FullSimplify[Solve[focNoMFNRPM,{w1,p2}],Assumptions->$Assumptions];
solNoMFNRPM=First@solNoMFNRPMAll



(* ::Input:: *)




(* ::Input:: *)
discRPMEq=<|"w1"->FullSimplify[w1/. solNoMFNRPM,Assumptions->$Assumptions],"w2"->FullSimplify[w2FromP2RPM[p2]/. solNoMFNRPM,Assumptions->$Assumptions],"p1"->FullSimplify[p1FromW1[w1]/. solNoMFNRPM,Assumptions->$Assumptions],"p2"->FullSimplify[p2/. solNoMFNRPM,Assumptions->$Assumptions],"q1"->FullSimplify[q1[p1FromW1[w1],p2]/. solNoMFNRPM,Assumptions->$Assumptions],"q2"->FullSimplify[q2[p2,p1FromW1[w1]]/. solNoMFNRPM,Assumptions->$Assumptions],"piU"->FullSimplify[piUNoMFNRPM[w1,p2]/. solNoMFNRPM,Assumptions->$Assumptions],"pi2"->0,"pi1"->0|>



(* ::Input:: *)



(* ::Input:: *)


(*-----------------------5. Case 4:MFN+RPM-----------------------*)
(*MFN:w1=w2=w,p1=w.RPM:U sets p2,but must satisfy D2 PC:p2>=w for q2>0. Under-1<\[Alpha]<1 (stable demand),for given w the objective is linear in p2 with coefficient (\[Alpha]-1),hence p2 is minimized=>binding PC:p2=w.Then U chooses w.*)



(* ::Input:: *)
(*test sign*)
 solpiUp22 =D[piU[w,w,p1,p2],p2]//FullSimplify



(* ::Input:: *)

p2MFNRPM[w_]:=w;

piUMFNRPM[w_]:=FullSimplify[piU[w,w,w,p2MFNRPM[w]],Assumptions->$Assumptions];


(* ::Input:: *)
focMFNRPM=FullSimplify[D[piUMFNRPM[w],w]==0,Assumptions->$Assumptions];
solMFNRPMAll=FullSimplify[Solve[focMFNRPM,w],Assumptions->$Assumptions];
solMFNRPM=First@solMFNRPMAll



(* ::Input:: *)

mfnRPMEq=<|"w1"->FullSimplify[w/. solMFNRPM,Assumptions->$Assumptions],"w2"->FullSimplify[w/. solMFNRPM,Assumptions->$Assumptions],"p1"->FullSimplify[w/. solMFNRPM,Assumptions->$Assumptions],"p2"->FullSimplify[p2MFNRPM[w]/. solMFNRPM,Assumptions->$Assumptions],"q1"->FullSimplify[q1[w,p2MFNRPM[w]]/. solMFNRPM,Assumptions->$Assumptions],"q2"->FullSimplify[q2[p2MFNRPM[w],w]/. solMFNRPM,Assumptions->$Assumptions],"piU"->FullSimplify[piUMFNRPM[w]/. solMFNRPM,Assumptions->$Assumptions],"pi2"->0,"pi1"->0|>


(* ::Input:: *)





(* ::Input:: *)


(*-----------------------6. Summary Grid (4 cases)-----------------------*)
summaryRows4={{"\:6279\:53d1\:4ef7 (w_1)",discEq["w1"],mfnEq["w1"],discRPMEq["w1"],mfnRPMEq["w1"]},{"\:6279\:53d1\:4ef7 (w_2)",discEq["w2"],mfnEq["w2"],discRPMEq["w2"],mfnRPMEq["w2"]},{"\:96f6\:552e\:4ef7 (p_1)",discEq["p1"],mfnEq["p1"],discRPMEq["p1"],mfnRPMEq["p1"]},{"\:96f6\:552e\:4ef7 (p_2)",discEq["p2"],mfnEq["p2"],discRPMEq["p2"],mfnRPMEq["p2"]},{"\:9500\:91cf (q_1)",discEq["q1"],mfnEq["q1"],discRPMEq["q1"],mfnRPMEq["q1"]},{"\:9500\:91cf (q_2)",discEq["q2"],mfnEq["q2"],discRPMEq["q2"],mfnRPMEq["q2"]},{"\:4e0a\:6e38\:5229\:6da6 (\[Pi]_U)",discEq["piU"],mfnEq["piU"],discRPMEq["piU"],mfnRPMEq["piU"]},{"\:7ecf\:9500\:55462\:5229\:6da6 (\[Pi]_2)",discEq["pi2"],mfnEq["pi2"],discRPMEq["pi2"],mfnRPMEq["pi2"]},{"\:7ecf\:9500\:55461\:5229\:6da6 (\[Pi]_1)",0,0,0,0}};

(*-----------------------7. Checks with hard-fail guard-----------------------*)
expectedKeys={"w1","w2","p1","p2","q1","q2","piU","pi2","pi1"};

checks={
   {"NoMFN+NoRPM association has expected keys",Keys[discEq]===expectedKeys},
   {"MFN+NoRPM association has expected keys",Keys[mfnEq]===expectedKeys},
   {"NoMFN+RPM association has expected keys",Keys[discRPMEq]===expectedKeys},
   {"MFN+RPM association has expected keys",Keys[mfnRPMEq]===expectedKeys},
   {"p2BR raw FOC is equivalent to best-response target form",p2BRTransformCheck},
   {"NoMFN+NoRPM FOCs hold at selected solution",TrueQ[FullSimplify[And@@(focNoMFNNoRPM/. solNoMFNNoRPM),Assumptions->$Assumptions]]},
   {"MFN+NoRPM FOC holds at selected solution",TrueQ[FullSimplify[focMFNNoRPM/. solMFNNoRPM,Assumptions->$Assumptions]]},
   {"NoMFN+RPM FOCs hold at selected solution",TrueQ[FullSimplify[And@@(focNoMFNRPM/. solNoMFNRPM),Assumptions->$Assumptions]]},
   {"MFN+RPM FOC holds at selected solution",TrueQ[FullSimplify[focMFNRPM/. solMFNRPM,Assumptions->$Assumptions]]},
   {"summaryRows4 contains nine economic objects",Length[summaryRows4]===9}
};

checkResults=Last/@checks;
checksAreBoolean=VectorQ[checkResults,BooleanQ];
allChecksTrue=TrueQ[checksAreBoolean&&And@@checkResults];

checksGrid=Grid[Prepend[checks,{"Check","Result"}],Frame->All,ItemStyle->Directive[14],Alignment->{Left,Center}]

If[!allChecksTrue,
   Print["CHECKS_FAILED_OR_MALFORMED"];
   Print[checks];
   Exit[1]
];

summaryGrid4=Grid[Prepend[summaryRows4,{"\:5bf9\:8c61","NoMFN+NoRPM","MFN+NoRPM","NoMFN+RPM","MFN+RPM"}],Frame->All,ItemStyle->Directive[14],Alignment->{Left,Center,Center,Center,Center}];

summaryGrid4



(* ::Input:: *)
(* Notebook-only styling cell removed for script execution:
   Insert[%49, Alignment -> Center, 2] *)


(* ::Input:: *)
(* Notebook-only styling cell removed for script execution:
   Insert[%50, {Background -> {None, {GrayLevel[0.7], {White}}},
      Dividers -> {Black, {2 -> Black}}, Frame -> True,
      Spacings -> {2, {2, {0.7}, 2}}}, 2] *)
