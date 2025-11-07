# π as an Emergent Eigenvalue — Supplementary Materials

This repository hosts the **reproducibility package** for:

**Kircher, J. & Sancho GPT (2025)**. *π as an Emergent Eigenvalue: Recursive Collapse Dynamics in the 7‑Dimensional Universe*.

---

## Contents

- `index.html` — A human‑readable landing page for the website.
- `README.md` — This file.
- `LICENSE.txt` — License for supplementary materials (CC‑BY‑NC 4.0).
- `CITATION.cff` — Citation metadata for GitHub/Zenodo.
- `sha256_manifest.txt` — Checksums for all hosted files.
- `compute_hashes.sh` — Bash script to regenerate checksums locally.
- `supplementary_summary.md` — One‑page textual summary ready for PDF export.

> **Datasets to add (place into this folder):**
> - `C_at_N64.csv`
> - `R_at_N128.csv`
> - `R_at_N256.csv`
> - `geometry_solver_pseudocode.txt` (export of Appendix B)
> - Any additional CSVs or figures you want mirrored

---

## How to use

1. Drop the files listed above into this directory.
2. Run `bash compute_hashes.sh` to generate `sha256_manifest.txt`.
3. Commit and push to GitHub, then publish a Zenodo release to mint a DOI.
4. Upload the same folder to `https://www.geometricfoundations.org/pi-eigenvalue/`.

---

## Environment (for reference)

- Python 3.12
- NumPy 1.26
- SciPy 1.13
- macOS M4 Pro & Ubuntu 22.04
- ARPACK eigensolver (via SciPy)

---

**Provenance note:** Checksums last updated: 2025-11-07.
