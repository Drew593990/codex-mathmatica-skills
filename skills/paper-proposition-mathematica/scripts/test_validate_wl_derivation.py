"""Protocol regression tests; real Wolfram integration is separately reported."""
import contextlib
import io
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import validate_wl_derivation as validator

class Workspace(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(dir=os.environ.get('WL_VALIDATION_TEST_ROOT'))
        self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)
        self.target=self.root/'sample.wl'
        self.target.write_text('checks={{"identity",True}};',encoding='utf-8')
    def cli(self,extra=()):
        output=io.StringIO()
        with patch.object(sys,'argv',['validate',str(self.target),*extra]),contextlib.redirect_stdout(output),contextlib.redirect_stderr(output):
            code=validator.main()
        return code,output.getvalue()

class ProtocolTests(Workspace):
    def test_missing_runtime(self):
        with patch.object(validator,'find_wolfram',return_value=None),patch.object(validator,'text_checks',return_value=[]):
            code,out=self.cli()
        self.assertEqual(code,4,out)
    def test_static_only(self):
        with patch.object(validator,'run_runtime_checks') as run:
            code,out=self.cli(['--no-runtime'])
        self.assertEqual(code,0,out)
        self.assertIn('RUNTIME_VALIDATION_NOT_REQUESTED',out)
        self.assertNotIn('RUNTIME_VALIDATION_OK',out)
        run.assert_not_called()
    def test_advisory_vs_strict(self):
        with patch.object(validator,'find_wolfram',return_value='fake'),patch.object(validator,'run_runtime_checks',return_value=(0,'checked\n')) as run:
            code,out=self.cli()
        self.assertEqual(code,0,out);run.assert_called_once()
        self.assertIn('STYLE_ADVISORY',out)
        self.assertEqual(self.cli(['--strict-style','--no-runtime'])[0],3)
    def test_first_and_benchmark_names_are_not_required_or_banned(self):
        self.target.write_text('ClearAll["Global`*"]; $Assumptions=True; FullSimplify[True]; Solve[x==0,x]; expectedResults=<||>; summaryRows={}; summaryGrid=Grid[summaryRows]; checks={{"ok",True}};',encoding='utf-8')
        self.assertEqual(validator.text_checks(self.target),[])
    def test_bad_inputs(self):
        self.target.unlink();self.assertEqual(self.cli(['--no-runtime'])[0],2)
        self.target.mkdir();self.assertEqual(self.cli(['--no-runtime'])[0],2)
        self.target.rmdir();self.target.write_bytes(b'\xff\xfe\x00')
        self.assertEqual(self.cli(['--no-runtime'])[0],2)
    def test_bad_timeout(self):
        for value in ('0','-1','nan','inf'):
            with self.subTest(value=value):self.assertEqual(self.cli(['--timeout',value,'--no-runtime'])[0],2)
    def test_executable_arguments(self):
        wrapper=self.root/'含空格.wl'
        for exe,flag in [('wolfram.exe','-script'),('WolframKernel.exe','-script'),('wolframscript.exe','-file'),('custom.exe','-script')]:
            self.assertEqual(validator.build_runtime_command(exe,wrapper),[exe,flag,str(wrapper)])
    def test_string_escaping(self):
        self.assertEqual(validator.wl_quote('a"b\\c'),'"a\\"b\\\\c"')
        self.assertEqual(validator.wl_quote('含'), 'FromCharacterCode[{21547}]')
        for bad in ('a\nb','a\rb','a\x00b'):
            with self.assertRaises(ValueError):validator.wl_quote(bad)
    def test_start_failure_and_timeout(self):
        for error,expected in [(OSError('not launchable'),4),(subprocess.TimeoutExpired(['fake'],1,output=b'partial result'),6)]:
            with self.subTest(expected=expected),patch.object(subprocess,'run',side_effect=error):
                code,out=validator.run_runtime_checks(self.target,'fake',work_dir=self.root)
                self.assertEqual(code,expected,out)
                self.assertIn('not launchable' if expected==4 else 'partial result',out)
                self.assertEqual(list(self.root.glob('wl-validate-*')),[])
    def test_protocol_statuses(self):
        statuses={'ok':0,'execution_failed':5,'missing_checks':21,'non_boolean':22,'failed_check':23,'empty_checks':24,'malformed_checks':25}
        for status,code in statuses.items():
            self.assertEqual(validator.classify_runtime_result(code,f'VALIDATION_RESULT:abc:{status}\n','abc')[0],code)
    def test_incomplete_or_inconsistent_protocol(self):
        cases=[(0,'',26),(0,'VALIDATION_OK\n',26),(0,'VALIDATION_RESULT:wrong:ok\n',26),(0,'VALIDATION_RESULT:abc:ok\nVALIDATION_RESULT:abc:ok\n',26),(0,'VALIDATION_RESULT:abc:mystery\n',26),(1,'VALIDATION_RESULT:abc:ok\n',26),(3221225477,'',5)]
        for native,out,expected in cases:
            with self.subTest(out=out):self.assertEqual(validator.classify_runtime_result(native,out,'abc')[0],expected)

class WolframTests(Workspace):
    def setUp(self):
        super().setUp()
        self.exe=os.environ.get('WL_VALIDATION_TEST_EXE')
        if not self.exe:self.skipTest('Real Wolfram tests not run: WL_VALIDATION_TEST_EXE unset')
    def run_wl(self,source):
        target=self.root/'含空格 sample.wl'
        target.write_text(source,encoding='utf-8')
        return validator.run_runtime_checks(target,self.exe,work_dir=self.root)
    def test_shapes(self):
        cases=[('checks={{"identity",True}};',0),('checks={};',24),('checks=3;',24),('Null;',21),('checks={{True}};',25),('checks={{"x",True,False}};',25),('checks={{" ",True}};',25),('checks={{"x",False}};',23),('checks={{"x",{True}}};',22),('checks={{"x",<|"k"->True|>}};',22),('checks={{"x",x>0}};',22),('checks={{"x",ConditionalExpression[True,a>0]}};',22)]
        for source,expected in cases:
            with self.subTest(source=source):
                code,out=self.run_wl(source);self.assertEqual(code,expected,out)
    def test_early_exit(self):
        for source in ('checks={{"bad",False}};Exit[0];','Print["VALIDATION_OK"];Exit[0];'):
            code,out=self.run_wl(source);self.assertEqual(code,26,out)
    def test_clearall_reduce_without_grid(self):
        code,out=self.run_wl('ClearAll["Global`*"]; r=Reduce[x==1,x,Reals]; checks={{"reduce",TrueQ[r==(x==1)]}};')
        self.assertEqual(code,0,out)
    def test_selection_styles(self):
        for select in ('selected=First[solutions];','{selected}=solutions;'):
            code,out=self.run_wl('solutions=Solve[x==1,x];If[Length[solutions]!=1,Exit[1]];'+select+'checks={{"FOC",TrueQ[(x/.selected)==1]}};')
            self.assertEqual(code,0,out)
    def test_syntax_abort_get_failure(self):
        for source in ('checks={{"ok",True}};broken[','Abort[];','Get["does-not-exist.wl"];'):
            with self.subTest(source=source):
                code,out=self.run_wl(source);self.assertNotEqual(code,0,out)
    def test_example_scope_counterexample(self):
        example=Path(__file__).resolve().parents[1]/'examples/mfn-rpm-nonash-competition-style.wl'
        source=f'Get[{validator.wl_quote(example.as_posix())}];'+r'''
point={a->2,c->10,\[Alpha]->0};
observed={discEq["q1"],discEq["q2"]}/.point;
checks={
 {"registered example checks",TrueQ[And@@(Last/@checks)]},
 {"point satisfies declared assumptions",TrueQ[$Assumptions/.point]},
 {"negative quantities delimit example scope",TrueQ[observed=={-9/2,-2}]}
};
'''
        code,out=self.run_wl(source);self.assertEqual(code,0,out)

if __name__=='__main__':unittest.main()