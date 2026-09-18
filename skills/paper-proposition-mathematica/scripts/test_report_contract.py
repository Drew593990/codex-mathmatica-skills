"""Regression tests for the report contract, including deliberate corruption."""
import copy
import hashlib
import json
import os
from pathlib import Path
import tempfile
import unittest
import subprocess
import sys

from validate_report_contract import validate


class ReportContractTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(dir=os.environ.get("REPORT_GATE_TEST_ROOT"))
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.tex = r"p_M=r+P(q_M,x_M)"
        self.catalog = {
            "price": {"tex": self.tex, "context": "market", "free_symbols": ["q_M", "x_M", "r"], "status": "conditional"},
            "foc": {"tex": r"F(q_M,x_M;r)=0", "context": "market", "free_symbols": ["q_M", "x_M", "r"], "status": "condition"},
        }
        self.report = "DEF_RHO\nBEGIN_BODY\n" + self.tex + "\nEND_BODY\nUSE_RHO\nBEGIN_TABLE\n" + self.tex + "\nEND_TABLE\nBEGIN_COND\nF(q_M,x_M;r)=0\nEND_COND"
        (self.root / "model.tex").write_text(self.report, encoding="utf-8")
        self.contract = {
            "version": 1,
            "catalog": {"file": "catalog.json", "sha256": ""},
            "contexts": {"market": {"forbidden_free_symbols": ["q", "x"]}},
            "requirements": [{"scenario": "market", "item": "price", "formula": "price", "placements": ["body", "result_table"], "conditions": ["foc"]}],
            "files": ["model.tex"],
            "occurrences": [
                {"formula": "price", "file": "model.tex", "begin": "BEGIN_BODY", "end": "END_BODY", "placement": "body"},
                {"formula": "price", "file": "model.tex", "begin": "BEGIN_TABLE", "end": "END_TABLE", "placement": "result_table"},
                {"formula": "foc", "file": "model.tex", "begin": "BEGIN_COND", "end": "END_COND", "placement": "condition_table"},
            ],
            "definitions": [{"symbol": "rho_total", "file": "model.tex", "definition": "DEF_RHO", "first_use": "USE_RHO"}],
        }
        self.save_catalog()

    def save_catalog(self):
        path = self.root / "catalog.json"
        path.write_text(json.dumps(self.catalog), encoding="utf-8")
        self.contract["catalog"]["sha256"] = hashlib.sha256(path.read_bytes()).hexdigest()

    def run_gate(self):
        return validate(self.contract, self.root)

    def test_optional_proof_metadata_preserves_formula_status(self):
        self.catalog['price'].update(
            status='conditional', proof_status='unresolved',
            proof_evidence='FOC candidate only; global optimality not established')
        self.save_catalog()
        self.assertEqual(self.run_gate(), [])

    def test_proof_status_cannot_replace_formula_status(self):
        self.catalog['price']['status'] = 'proved'
        self.save_catalog()
        errors = self.run_gate()
        self.assertTrue(any('missing/invalid status' in item for item in errors))

    def test_valid(self):
        self.assertEqual(self.run_gate(), [])

    def test_body_loses_subscript_while_table_stays_correct(self):
        (self.root / "model.tex").write_text(self.report.replace(self.tex, r"p_M=r+P(q,x)", 1), encoding="utf-8")
        self.assertTrue(self.run_gate())

    def test_wrong_superscript(self):
        (self.root / "model.tex").write_text(self.report.replace("p_M", "p^S", 1), encoding="utf-8")
        self.assertTrue(self.run_gate())

    def test_missing_result_table(self):
        self.contract["occurrences"].pop(1)
        self.assertTrue(self.run_gate())

    def test_missing_body(self):
        self.contract["occurrences"].pop(0)
        self.assertTrue(self.run_gate())

    def test_missing_conditions(self):
        self.contract["occurrences"].pop()
        self.assertTrue(self.run_gate())

    def test_missing_scenario_item(self):
        self.contract["requirements"].append({"scenario": "social", "item": "welfare", "formula": "missing", "placements": ["result_table"], "conditions": ["foc"]})
        self.assertTrue(self.run_gate())

    def test_canonical_unsubstituted_symbol(self):
        self.catalog["price"]["free_symbols"].append("q")
        self.save_catalog()
        self.assertTrue(self.run_gate())

    def test_generic_derivation_not_forced_to_equilibrium(self):
        self.contract["contexts"]["generic"] = {"forbidden_free_symbols": []}
        self.catalog["foc"].update(tex="F(q,x;r)=0", context="generic", free_symbols=["q", "x", "r"])
        (self.root / "model.tex").write_text(self.report.replace("F(q_M,x_M;r)=0", "F(q,x;r)=0"), encoding="utf-8")
        self.save_catalog()
        self.assertEqual(self.run_gate(), [])

    def test_missing_status(self):
        del self.catalog["price"]["status"]
        self.save_catalog()
        self.assertTrue(self.run_gate())

    def test_unsolved_must_have_explanation(self):
        self.catalog["price"]["status"] = "unsolved"
        self.save_catalog()
        self.assertTrue(self.run_gate())

    def test_unsolved_with_explanation_is_allowed(self):
        self.catalog["price"].update(status="unsolved", explanation="The system has not been solved.")
        self.save_catalog()
        self.assertEqual(self.run_gate(), [])

    def test_stale_catalog_hash(self):
        self.contract["catalog"]["sha256"] = "0" * 64
        self.assertTrue(self.run_gate())

    def test_definition_after_use(self):
        self.contract["definitions"][0].update(definition="USE_RHO", first_use="DEF_RHO")
        self.assertTrue(self.run_gate())

    def test_duplicate_marker(self):
        (self.root / "model.tex").write_text(self.report + "\nBEGIN_BODY", encoding="utf-8")
        self.assertTrue(self.run_gate())

    def test_unlisted_document(self):
        self.contract["files"] = []
        self.assertTrue(self.run_gate())

    def test_empty_requirements(self):
        self.contract["requirements"] = []
        self.assertTrue(self.run_gate())

    def test_empty_occurrences(self):
        self.contract["occurrences"] = []
        self.assertTrue(self.run_gate())

    def test_duplicate_requirement(self):
        self.contract["requirements"].append(copy.deepcopy(self.contract["requirements"][0]))
        self.assertTrue(self.run_gate())

    def test_path_escape(self):
        self.contract["catalog"]["file"] = "../escape.json"
        self.assertTrue(self.run_gate())

    def test_unknown_context(self):
        self.catalog["price"]["context"] = "unknown"
        self.save_catalog()
        self.assertTrue(self.run_gate())

    def test_conditions_cannot_replace_results(self):
        self.contract["requirements"][0]["placements"] = ["condition_table"]
        self.assertTrue(self.run_gate())

    def test_cli_exit_status_and_json(self):
        contract = self.root / "contract.json"
        output = self.root / "check.json"
        command = [sys.executable, str(Path(__file__).with_name("validate_report_contract.py")), str(contract), "--root", str(self.root), "--output", str(output)]
        contract.write_text(json.dumps(self.contract), encoding="utf-8")
        result = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(json.loads(output.read_text())["mechanical_checks_passed"])
        (self.root / "model.tex").write_text(self.report.replace(self.tex, "P(q,x)", 1), encoding="utf-8")
        result = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertFalse(json.loads(output.read_text())["mechanical_checks_passed"])

    def test_tex_command_separator_is_not_discarded(self):
        self.catalog["price"]["tex"] = r"\alpha q_M"
        self.save_catalog()
        (self.root / "model.tex").write_text(self.report.replace(self.tex, r"\alphaq_M"), encoding="utf-8")
        self.assertTrue(self.run_gate())

    def test_malformed_contract(self):
        self.assertTrue(validate({}, self.root))


if __name__ == "__main__":
    unittest.main()
