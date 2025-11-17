# AoC-137 Supplementary Materials

This directory contains all reproducible materials supporting:

**AoC_Dev_137_1.0.pdf**  
*Deriving α ≈ 1/137 from a Stable Geometric Fixed Point*

---

## Included Materials

### 🔢 Numerical Data  
- `alpha_137_numerics.json` — locked numerical outputs  
- `locks.json` — canonical parameter lockfile  
- `hash_manifest.txt` (optional) — SHA256 integrity record  

### 🧮 Reproducibility Scripts  
- `verify_alpha_locks.py` — full bit-for-bit verification  
- `generate_137_figures.py` — regenerates Figures 1–3  
- `AoC_137_Workbook.ipynb` — Google Colab-compatible notebook  

### 📊 Figures  
- `figure1_hybrid.png`  
- `figure2_hybrid.png`  
- `figure3_hybrid.png`  
- `alpha_complete_analysis.png`  
- `alpha_derivation_landscape.png`  

### 🧪 Environment  
- `environment.yml` — exact solver environment  

### 📚 Citation  
- `CITATION.cff` — interoperable citation metadata  

---

## Usage

Run the verification:
python verify_alpha_locks.py
Regenerate all published figures:

python generate_137_figures.py
Open the notebook (local or Colab):

AoC_137_Workbook.ipynb
---

## Repository Link  
Main paper is located in:

➡️ (https://github.com/jedijkq/7dU_Seed/blob/main/papers/AoC_Dev_137_1.0.pdf)
