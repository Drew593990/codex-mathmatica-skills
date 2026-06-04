#!/usr/bin/env python3
"""Validate a Mathematica/Wolfram derivation script for this skill.

The validator performs text-level style checks and, when a Wolfram runtime is
provided or discoverable, runtime checks that the script defines `checks` whose
results are all Boolean True.
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


STYLE_TOKENS = [
    'ClearAll["Global`*"]',
    "$Assumptions",
    "FullSimplify",
    "Solve",
    "summaryRows",
    "summaryGrid",
    "Grid[",
    "checks",
]


def find_wolfram(explicit: str | None) -> str | None:
    if explicit:
        return explicit
    for env_name in ("WOLFRAM_EXE", "WOLFRAM_KERNEL", "WOLFRAMSCRIPT"):
        value = os.environ.get(env_name)
        if value and Path(value).exists():
            return value
    for cmd in ("wolfram", "WolframKernel", "wolframscript"):
        found = shutil.which(cmd)
        if found:
            return found
    return None


def text_checks(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8", errors="replace")
    compact = re.sub(r"\s+", "", text)
    failures: list[str] = []
    for token in STYLE_TOKENS:
        if token not in text:
            failures.append(f"missing style token: {token}")
    if "Association[" not in text and "<|" not in text:
        failures.append("missing association result object: Association[...] or <|...|>")
    if "First@" not in compact and "First[" not in text:
        failures.append("missing selected-solution pattern: First @, First@, or First[")
    if "Exit[1]" not in text:
        failures.append("missing hard-fail Exit[1] block")
    if "VectorQ" not in text or "BooleanQ" not in text:
        failures.append("missing BooleanQ/VectorQ malformed-check guard")
    if "And@@(Last/@checks)" not in compact and "And@@checkResults" not in compact:
        failures.append("missing all-checks-true guard")
    if re.search(r"expected\w*(?:Eq|Results?)\s*=\s*(?:Association\[|<\|)", text, re.IGNORECASE):
        failures.append(
            "avoid hand-entered expected answer associations; use primitive-consistency checks or labeled paperClaim... benchmarks"
        )
    if re.search(r"numeric\w*\s*==\s*(?:Association\[|<\|)", text, re.IGNORECASE):
        failures.append(
            "avoid hand-entered numeric benchmark associations; compare against independent numeric solving or labeled paperNumericClaim... benchmarks"
        )
    if re.search(r'\{\s*"[^"]+"\s*,\s*And\s*@@', text):
        failures.append(
            "avoid raw And @@ inside checks; wrap symbolic conjunctions with TrueQ[FullSimplify[..., Assumptions -> ass]]"
        )
    return failures


def run_runtime_checks(path: Path, wolfram: str) -> tuple[int, str]:
    target = str(path).replace("\\", "\\\\")
    validator = f"""
targetPath = "{target}";
Get[targetPath];
If[! ValueQ[checks],
   Print["VALIDATION_FAILED: checks is not defined"];
   Exit[21]
];
checkResults = Last /@ checks;
If[! VectorQ[checkResults, BooleanQ],
   Print["VALIDATION_FAILED: checks contains non-Boolean results"];
   Print[InputForm[checks]];
   Exit[22]
];
If[! TrueQ[And @@ checkResults],
   Print["VALIDATION_FAILED: at least one check is False"];
   Print[InputForm[checks]];
   Exit[23]
];
Print["VALIDATION_OK"];
Exit[0];
"""
    with tempfile.NamedTemporaryFile("w", suffix=".wl", delete=False, encoding="utf-8") as f:
        f.write(validator)
        temp_path = f.name
    try:
        proc = subprocess.run(
            [wolfram, "-script", temp_path],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=180,
        )
        return proc.returncode, proc.stdout
    finally:
        try:
            Path(temp_path).unlink()
        except OSError:
            pass


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("wl_path", type=Path)
    parser.add_argument("--wolfram", default=None)
    parser.add_argument("--no-runtime", action="store_true")
    args = parser.parse_args()

    if not args.wl_path.exists():
        print(f"missing file: {args.wl_path}", file=sys.stderr)
        return 2

    failures = text_checks(args.wl_path)
    if failures:
        print("TEXT_VALIDATION_FAILED")
        for failure in failures:
            print(f"- {failure}")
        return 3

    if args.no_runtime:
        print("TEXT_VALIDATION_OK")
        return 0

    wolfram = find_wolfram(args.wolfram)
    if not wolfram:
        print("TEXT_VALIDATION_OK")
        print("RUNTIME_VALIDATION_SKIPPED: Wolfram runtime not found")
        return 0

    code, output = run_runtime_checks(args.wl_path, wolfram)
    print(output, end="")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
