# π-Eigenvalue Supplementary Files

This archive contains the primary data and pseudocode supporting the paper:
> Kircher, J., & Sancho GPT (2025). *π as an Emergent Eigenvalue: Recursive Collapse Dynamics in the 7‑Dimensional Universe.*

### Files Included
- C_at_N64.csv — Independent replication dataset (C@)
- R_at_N128.csv — Main production run (N=128)
- R_at_N256.csv — High‑resolution convergence test
- geometry_solver_pseudocode.txt — Iterative solver algorithm

All CSVs share the schema: α, ξ, σ, λ̃₁, λ₁^(phys), Δ, status

Software environment: Python 3.12 + NumPy 1.26 + SciPy 1.13 (ARPACK)

## Provenance & Verification

All supplementary files in this directory were archived and hashed on November 6, 2025.  
Verification hashes are recorded in `sha256_manifest.txt`.

Users may verify file integrity via:

    sha256sum -c sha256_manifest.txt

If all entries report “OK”, the dataset and pseudocode are verified as authentic and unmodified.
