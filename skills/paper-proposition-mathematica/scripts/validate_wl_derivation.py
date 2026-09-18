#!/usr/bin/env python3
"""Check WL style hints and the completion of registered Boolean runtime checks.

This is neither a proof checker nor a sandbox. --no-runtime is explicit static
inspection; style hints are advisory unless --strict-style is requested.
"""
from __future__ import annotations
import argparse
import math
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import uuid

STYLE_TOKENS = ['ClearAll["Global`*"]', '$Assumptions', 'FullSimplify', 'Solve',
                'summaryRows', 'summaryGrid', 'Grid[', 'checks']


def find_wolfram(explicit: str | None) -> str | None:
    if explicit:
        return explicit
    for name in ('WOLFRAM_EXE', 'WOLFRAM_KERNEL', 'WOLFRAMSCRIPT'):
        value=os.environ.get(name)
        if value and Path(value).is_file():
            return value
    for name in ('wolfram', 'WolframKernel', 'wolframscript'):
        value=shutil.which(name)
        if value:
            return value
    return None


def text_checks(path: Path) -> list[str]:
    """Heuristic full-paper style hints, not syntax or mathematical validation."""
    text=path.read_text(encoding='utf-8-sig')
    hints=[f'missing conventional style token: {token}' for token in STYLE_TOKENS if token not in text]
    if 'Association[' not in text and '<|' not in text:
        hints.append('missing conventional association result object')
    return hints


def wl_quote(value: str) -> str:
    if any(c in value for c in ('\n', '\r', '\x00')):
        raise ValueError('Wolfram paths/markers cannot contain newline or NUL')
    # ASCII wrapper input avoids Windows kernel decoding of raw Unicode paths.
    if not value.isascii():
        return 'FromCharacterCode[{' + ','.join(str(ord(c)) for c in value) + '}]'
    return '"' + value.replace('\\', '\\\\').replace('"', '\\"') + '"'


def build_wrapper(path: Path, run_id: str) -> str:
    def finish(status: str, code: int) -> str:
        return f'Print[{wl_quote(f"VALIDATION_RESULT:{run_id}:{status}")}]; Exit[{code}]'
    target=wl_quote(path.resolve().as_posix())
    return f'''
loaded = CheckAbort[Get[{target}], $Aborted];
If[MemberQ[{{$Failed, $Aborted}}, loaded], {finish('execution_failed', 5)}];
If[!ValueQ[Global`checks], {finish('missing_checks', 21)}];
If[!ListQ[Global`checks] || Length[Global`checks] == 0,
   Print[InputForm[Global`checks]]; {finish('empty_checks', 24)}];
If[!AllTrue[Global`checks,
   MatchQ[#, {{_String, _}}] && StringLength[StringTrim[First[#]]] > 0 &],
   Print[InputForm[Global`checks]]; {finish('malformed_checks', 25)}];
checkResults = Last /@ Global`checks;
If[!VectorQ[checkResults, BooleanQ],
   Print[InputForm[Global`checks]]; {finish('non_boolean', 22)}];
If[!TrueQ[And @@ checkResults],
   Print[InputForm[Global`checks]]; {finish('failed_check', 23)}];
{finish('ok', 0)};
'''


def build_runtime_command(wolfram: str, wrapper: Path) -> list[str]:
    flag='-file' if Path(wolfram).stem.casefold()=='wolframscript' else '-script'
    return [wolfram, flag, str(wrapper)]


def classify_runtime_result(returncode: int, output: str, run_id: str) -> tuple[int, str]:
    expected={'ok':0, 'execution_failed':5, 'missing_checks':21, 'non_boolean':22,
              'failed_check':23, 'empty_checks':24, 'malformed_checks':25}
    prefix=f'VALIDATION_RESULT:{run_id}:'
    states=[line[len(prefix):] for line in output.splitlines() if line.startswith(prefix)]
    if not states:
        code=26 if returncode==0 else 5
        return code, output+f'\nRUNTIME_INCOMPLETE: native_exit={returncode}\n'
    if len(states)!=1 or states[0] not in expected:
        return 26, output+'\nRUNTIME_PROTOCOL_INVALID\n'
    code=expected[states[0]]
    if returncode!=code:
        return 26, output+f'\nRUNTIME_EXIT_MISMATCH: native_exit={returncode}\n'
    return code, output


def run_runtime_checks(path: Path, wolfram: str, *, timeout: float=180.0,
                       work_dir: Path | None=None) -> tuple[int, str]:
    if not math.isfinite(timeout) or timeout<=0:
        return 2, 'INVALID_INPUT: timeout must be finite and positive\n'
    run_id=uuid.uuid4().hex
    temp=None
    try:
        wrapper_text=build_wrapper(path,run_id)
        parent=Path(work_dir).resolve() if work_dir is not None else Path(tempfile.gettempdir()).resolve()
        parent.mkdir(parents=True,exist_ok=True)
        temp=Path(tempfile.mkdtemp(prefix='wl-validate-',dir=parent)).resolve()
        wrapper=temp/'wrapper.wl'
        wrapper.write_text(wrapper_text,encoding='utf-8')
        command=build_runtime_command(wolfram,wrapper)
        try:
            proc=subprocess.run(command,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,
                                text=True,encoding='utf-8',errors='replace',timeout=timeout,
                                shell=False)
        except subprocess.TimeoutExpired as error:
            partial=error.stdout or ''
            if isinstance(partial,bytes):partial=partial.decode('utf-8',errors='replace')
            return 6, partial+f'\nRUNTIME_TIMEOUT: timeout={timeout}; command={command!r}\n'
        except OSError as error:
            return 4, f'RUNTIME_UNAVAILABLE: {error}; command={command!r}\n'
        code,output=classify_runtime_result(proc.returncode,proc.stdout,run_id)
        return code, f'RUNTIME_COMMAND: {command!r}\nNATIVE_EXIT: {proc.returncode}\n'+output
    except (OSError,ValueError) as error:
        return 2, f'INVALID_INPUT: {error}\n'
    finally:
        if temp is not None:
            # Only remove the private directory created by this invocation.
            if temp.parent!=parent or not temp.is_relative_to(parent):
                raise RuntimeError('Refusing cleanup outside validation directory')
            shutil.rmtree(temp)


def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('wl_path',type=Path)
    parser.add_argument('--wolfram',default=None)
    parser.add_argument('--no-runtime',action='store_true')
    parser.add_argument('--strict-style',action='store_true')
    parser.add_argument('--timeout',type=float,default=180.0)
    parser.add_argument('--work-dir',type=Path,default=None)
    args=parser.parse_args()
    if not args.wl_path.is_file() or not math.isfinite(args.timeout) or args.timeout<=0:
        print('INVALID_INPUT: provide a readable file and finite positive timeout',file=sys.stderr)
        return 2
    try:
        hints=text_checks(args.wl_path)
    except (OSError,UnicodeError) as error:
        print(f'INVALID_INPUT: {error}',file=sys.stderr)
        return 2
    if hints:
        print('TEXT_VALIDATION_FAILED' if args.strict_style else 'STYLE_ADVISORY')
        for hint in hints:print(f'- {hint}')
        if args.strict_style:return 3
    if args.no_runtime:
        print('TEXT_VALIDATION_OK: heuristic inspection only; not a syntax or proof check')
        print('RUNTIME_VALIDATION_NOT_REQUESTED')
        return 0
    wolfram=find_wolfram(args.wolfram)
    if not wolfram:
        print('RUNTIME_VALIDATION_UNAVAILABLE: Wolfram runtime not found')
        return 4
    code,output=run_runtime_checks(args.wl_path,wolfram,timeout=args.timeout,work_dir=args.work_dir)
    print(output,end='' if output.endswith('\n') else '\n')
    if code==0:
        print('RUNTIME_VALIDATION_OK: registered Boolean checks passed; proof scope requires review')
        print('VALIDATION_OK')
    return code


if __name__=='__main__':
    raise SystemExit(main())