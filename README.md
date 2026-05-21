# Codex Mathematica Skills

Two Codex skills for Wolfram/Mathematica-based mathematical modeling and economics paper proposition replication.

## Skills

- `mathmatica-user`: general Wolfram Language modeling, symbolic derivation, equilibrium solving, formula verification, and numeric simulation.
- `paper-proposition-mathematica`: economics paper proposition replication style, including notation, section structure, result associations, summary grids, checks, and plotting conventions.

The spelling `mathmatica-user` is intentional because it matches the original skill trigger used in the local workflow.

## Installation

Copy the desired skill folder into your Codex skills directory:

```powershell
Copy-Item -Recurse .\skills\mathmatica-user $env:CODEX_HOME\skills\
Copy-Item -Recurse .\skills\paper-proposition-mathematica $env:CODEX_HOME\skills\
```

If `CODEX_HOME` is not set, copy the folders into your local Codex skills directory manually.

## Wolfram Runtime

These skills assume a local Wolfram installation. Replace examples such as:

```powershell
& '<path-to-wolfram>\wolfram.exe' -script '<absolute-path-to-script.wl>'
```

with the actual path on your machine.

## Notes

- These skills are workflow templates. They do not include Wolfram/Mathematica itself.
- Generated derivation scripts should be run locally and verified with explicit checks before results are treated as reproduced.
- The paper proposition skill includes an additional style guide under `references/`.

## License

MIT License. See [LICENSE](LICENSE).
