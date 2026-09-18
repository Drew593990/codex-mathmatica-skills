"""Check registered report formulas and coverage, not mathematical truth.

The catalog must come from the named symbolic results, not from scraping the
report being checked. Unregistered prose/formulas still need a full review.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys


def normalize(text):
    # Preserve token-separating spaces: '\\alpha q' is not '\\alphaq'.
    return re.sub(r"\s+", " ", text).strip()


def validate(contract, root):
    errors = []
    root = Path(root).resolve()

    def require(ok, message):
        if not ok:
            errors.append(message)

    def path(name):
        candidate = (root / name).resolve()
        if Path(name).is_absolute() or not candidate.is_relative_to(root):
            raise ValueError("Path outside project: " + str(name))
        return candidate

    try:
        require(contract["version"] == 1, "Unsupported contract version")
        source = path(contract["catalog"]["file"])
        require(hashlib.sha256(source.read_bytes()).hexdigest() == contract["catalog"]["sha256"], "Catalog hash is stale")
        catalog = json.loads(source.read_text(encoding="utf-8-sig"))
        require(isinstance(catalog, dict) and bool(catalog), "Empty formula catalog")
        files = contract["files"]
        require(isinstance(files, list) and bool(files), "Report file inventory is empty")
        documents = {name: path(name).read_text(encoding="utf-8-sig") for name in files}
        contexts = contract["contexts"]
        for name, formula in catalog.items():
            require(isinstance(formula["tex"], str) and bool(formula["tex"].strip()), name + ": missing expression")
            status = formula.get("status")
            require(status in {"explicit", "conditional", "unsolved", "not_applicable", "condition", "identity"}, name + ": missing/invalid status")
            if status in {"unsolved", "not_applicable"}:
                require(bool(formula.get("explanation", "").strip()), name + ": missing explanation")
            context = formula["context"]
            require(context in contexts, name + ": unknown evaluation context")
            symbols = formula["free_symbols"]
            require(isinstance(symbols, list) and all(isinstance(s, str) for s in symbols), name + ": invalid symbol inventory")
            forbidden = contexts.get(context, {}).get("forbidden_free_symbols", [])
            require(not set(symbols).intersection(forbidden), name + ": unsubstituted symbols in named result")

        occurrences = contract["occurrences"]
        require(isinstance(occurrences, list) and bool(occurrences), "Formula occurrence inventory is empty")
        found = set()
        for occurrence in occurrences:
            name, file = occurrence["formula"], occurrence["file"]
            require(name in catalog, "Unknown formula: " + name)
            require(file in documents, "Unlisted report file: " + file)
            placement = occurrence["placement"]
            require(placement in {"body", "result_table", "condition_table", "caption", "conclusion"}, "Unknown placement: " + placement)
            if name not in catalog or file not in documents:
                continue
            text = documents[file]
            begin, end = occurrence["begin"], occurrence["end"]
            if not begin or not end or begin == end or text.count(begin) != 1 or text.count(end) != 1:
                errors.append(name + ": missing/ambiguous occurrence markers in " + file)
                continue
            start = text.index(begin) + len(begin)
            stop = text.index(end)
            require(start <= stop, name + ": reversed markers")
            require(normalize(text[start:stop]) == normalize(catalog[name]["tex"]), name + ": report differs from canonical expression in " + file + " (" + placement + ")")
            found.add((name, placement))

        requirements = contract["requirements"]
        require(isinstance(requirements, list) and bool(requirements), "Required scenario/item inventory is empty")
        seen = set()
        for requirement in requirements:
            pair = (requirement["scenario"], requirement["item"])
            require(all(pair), "Empty scenario/item")
            require(pair not in seen, "Duplicate scenario/item: " + str(pair))
            seen.add(pair)
            name = requirement["formula"]
            require(name in catalog, "Missing required result: " + str(pair))
            require("result_table" in requirement["placements"], name + ": result table required; conditions are not results")
            require(set(requirement["placements"]) <= {"body", "result_table", "caption", "conclusion"}, name + ": invalid result placement")
            for placement in requirement["placements"]:
                require((name, placement) in found, name + ": missing " + placement)
            conditions = requirement["conditions"]
            if catalog.get(name, {}).get("status") not in {"unsolved", "not_applicable"}:
                require(bool(conditions), name + ": defining/validity conditions required")
            for condition in conditions:
                require(condition in catalog and catalog[condition]["status"] == "condition", name + ": invalid condition record")
                require((condition, "condition_table") in found, name + ": missing condition table entry " + condition)

        for definition in contract["definitions"]:
            file = definition["file"]
            require(file in documents, "Definition file is not inventoried")
            if file not in documents:
                continue
            text = documents[file]
            before, use = definition["definition"], definition["first_use"]
            if not before or not use or text.count(before) != 1 or text.count(use) != 1:
                errors.append(definition["symbol"] + ": missing/ambiguous definition/use anchors")
                continue
            require(text.index(before) <= text.index(use), definition["symbol"] + ": definition follows first use")
    except (KeyError, TypeError, ValueError, OSError, AttributeError) as exc:
        errors.append("Invalid contract or missing input: " + str(exc))
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("contract", type=Path)
    parser.add_argument("--root", required=True, type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        contract = json.loads(args.contract.read_text(encoding="utf-8-sig"))
        errors = validate(contract, args.root)
    except (OSError, ValueError) as exc:
        errors = [str(exc)]
    result = {"mechanical_checks_passed": not errors, "errors": errors,
              "scope": "Registered expressions/placements only. Not a proof, completeness oracle, or PDF review."}
    rendered = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered)
    return int(bool(errors))


if __name__ == "__main__":
    sys.exit(main())
