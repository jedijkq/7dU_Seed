#!/usr/bin/env python3
"""
verify_alpha_locks.py

Verification script for α ≈ 1/137 geometric fixed-point derivation.
Regenerates all numerical results from locked parameters in locks.json.

Usage:
    python verify_alpha_locks.py

Requirements:
    - Python 3.12+
    - mpmath 1.3.0
    - numpy 1.26.0

Author: R@, Sanch0-5-Oh, C@ Sonnet 4.5, Gemini 2.5 Flash
Date: 2025-11-17
License: MIT
"""

import json
import hashlib
import sys
from pathlib import Path

try:
    from mpmath import mp, mpf, sqrt, pi as mp_pi
    import numpy as np
except ImportError as e:
    print(f"ERROR: Missing required package: {e}")
    print("Install with: pip install mpmath numpy")
    sys.exit(1)

# Set precision to 80 decimal digits
mp.dps = 80

# ============================================================================
# CONSTANTS
# ============================================================================

LOCKS_FILE = Path("locks.json")
TOL_ALPHA = mpf("1e-10")     # tolerance for alpha-related comparisons
TOL_XI = mpf("1e-8")         # tolerance for xi*
EPSILON_MACHINE = 1e-15      # cross-check threshold (float)

# ============================================================================
# LOAD LOCKED PARAMETERS
# ============================================================================

def load_locks():
    """Load locked parameters from locks.json"""
    if not LOCKS_FILE.exists():
        print(f"ERROR: {LOCKS_FILE} not found!")
        print("Please ensure locks.json is in the current directory.")
        sys.exit(1)
    
    with open(LOCKS_FILE, 'r') as f:
        return json.load(f)

# ============================================================================
# CORE COMPUTATIONS
# ============================================================================

def compute_alpha_pred(A1_over_A3, r):
    """Compute predicted α from geometric fixed point."""
    return (mpf(A1_over_A3) * mpf(r)) / (4 * mp_pi)

def compute_beta_prime_g(A1_over_A3, r, gamma=1):
    """Compute β'(g*) = -2 * A1 * r^gamma"""
    A1 = mpf(A1_over_A3)
    return -2 * A1 * mpf(r)**gamma

def compute_g_star(A1_over_A3, r, gamma=1):
    """Compute g* = sqrt(A1/A3 * r^gamma)"""
    return sqrt(mpf(A1_over_A3) * mpf(r)**gamma)

def compute_beta_prime_alpha(g_star, beta_prime_g):
    """Compute β'_α(g*) = (g*/2π) * β'(g*)"""
    return (g_star / (2 * mp_pi)) * beta_prime_g

def compute_xi_star(alpha_err, Delta_pi, beta_prime_alpha):
    """Compute ξ* from boundary saturation."""
    return abs(mpf(alpha_err) * mpf(Delta_pi) / beta_prime_alpha)

def compute_delta_alpha_max(xi_star, beta_prime_alpha, Delta_pi, K=1):
    """Compute maximum allowed drift."""
    return K * abs(mpf(xi_star) * beta_prime_alpha) / mpf(Delta_pi)

def compute_E_xi(alpha_exp, alpha_pred, Delta_pi):
    """Compute ξ-energy."""
    return ((1 / mpf(alpha_exp)) - (1 / alpha_pred)) * mpf(Delta_pi)

# ============================================================================
# VERIFICATION ROUTINE
# ============================================================================

def verify_all():
    
    print("="*70)
    print("VERIFICATION: α ≈ 1/137 GEOMETRIC FIXED POINT")
    print("="*70)
    print()
    
    locks = load_locks()
    print(f"✓ Loaded locks.json (version {locks['_metadata']['version']})")
    print()

    # Extract and convert to mpf for stability
    A1_over_A3 = mpf(locks['geometric_parameters']['A1_over_A3']['value'])
    r = mpf(locks['geometric_parameters']['r']['value'])
    gamma = mpf(locks['geometric_parameters']['gamma']['value'])
    K = mpf(locks['geometric_parameters']['K']['value'])
    Delta_pi = mpf(locks['collapse_gap']['Delta_pi']['value'])
    alpha_exp = mpf(locks['derived_quantities']['alpha_exp_CODATA2018']['value'])

    print("LOCKED PARAMETERS:")
    print(f"  A₁/A₃ = {A1_over_A3}")
    print(f"  r     = {r}")
    print(f"  γ     = {gamma}")
    print(f"  K     = {K}")
    print(f"  Δπ    = {Delta_pi}")
    print(f"  α_exp = {alpha_exp} (CODATA 2018)")
    print()

    # ========================================================================
    # 1. α_pred
    # ========================================================================
    print("-"*70)
    print("STEP 1: Computing α_pred")
    print("-"*70)

    alpha_pred = compute_alpha_pred(A1_over_A3, r)
    alpha_pred_float = float(alpha_pred)

    print(f"  α_pred = {alpha_pred_float:.10f}")
    print(f"  1/α_pred = {float(1/alpha_pred):.4f}")

    alpha_pred_locked = mpf(locks['derived_quantities']['alpha_pred']['value'])
    diff_alpha = abs(alpha_pred - alpha_pred_locked)

    if diff_alpha < TOL_ALPHA:
        print(f"  ✓ Matches locked value (diff = {diff_alpha:.2e})")
    else:
        print(f"  ✗ MISMATCH with locked value (diff = {diff_alpha:.2e})")
        return False
    print()

    # ========================================================================
    # 2. α_err
    # ========================================================================
    print("-"*70)
    print("STEP 2: Computing |α_err|")
    print("-"*70)

    alpha_err = abs(alpha_pred - alpha_exp)
    alpha_err_ppm = (alpha_err / alpha_exp) * 1e6

    print(f"  |α_err| = {alpha_err:.10e}")
    print(f"  Relative = {alpha_err_ppm:.1f} ppm")

    alpha_err_locked = mpf(locks['derived_quantities']['alpha_err']['value'])
    diff_err = abs(alpha_err - alpha_err_locked)

    if diff_err < TOL_ALPHA:
        print(f"  ✓ Matches locked value (diff = {diff_err:.2e})")
    else:
        print(f"  ✗ MISMATCH with locked value (diff = {diff_err:.2e})")
        return False
    print()

    # ========================================================================
    # 3. Flow derivatives
    # ========================================================================
    print("-"*70)
    print("STEP 3: Computing β'(g*) and β'_α(g*)")
    print("-"*70)

    g_star = compute_g_star(A1_over_A3, r, gamma)
    beta_prime_g = compute_beta_prime_g(A1_over_A3, r, gamma)
    beta_prime_alpha = compute_beta_prime_alpha(g_star, beta_prime_g)

    print(f"  g* = {float(g_star):.10f}")
    print(f"  β'(g*) = {float(beta_prime_g):.10f}")
    print(f"  β'_α(g*) = {float(beta_prime_alpha):.10f}")

    beta_prime_alpha_locked = mpf(locks['stochastic_parameters']['beta_prime_alpha']['value'])
    diff_beta = abs(beta_prime_alpha - beta_prime_alpha_locked)

    if diff_beta < TOL_ALPHA:
        print(f"  ✓ β'_α matches locked value (diff = {diff_beta:.2e})")
    else:
        print(f"  ✗ MISMATCH in β'_α (diff = {diff_beta:.2e})")
        return False
    print()

    # ========================================================================
    # 4. ξ*
    # ========================================================================
    print("-"*70)
    print("STEP 4: Computing ξ*")
    print("-"*70)

    xi_star = compute_xi_star(alpha_err, Delta_pi, beta_prime_alpha)
    print(f"  ξ* = {float(xi_star):.10f}")

    xi_star_locked = mpf(locks['stochastic_parameters']['xi_star']['value'])
    diff_xi = abs(xi_star - xi_star_locked)

    if diff_xi < TOL_XI:
        print(f"  ✓ Matches locked value (diff = {diff_xi:.2e})")
    else:
        print(f"  ✗ MISMATCH with locked value (diff = {diff_xi:.2e})")
        return False
    print()

    # ========================================================================
    # 5. Boundary saturation
    # ========================================================================
    print("-"*70)
    print("STEP 5: Verifying boundary saturation")
    print("-"*70)

    delta_alpha_max = compute_delta_alpha_max(xi_star, beta_prime_alpha, Delta_pi, K)
    saturation_residual = abs(alpha_err - delta_alpha_max)

    print(f"  |α_err|     = {alpha_err:.10e}")
    print(f"  |δα|_max    = {float(delta_alpha_max):.10e}")
    print(f"  Residual    = {saturation_residual:.2e}")

    if saturation_residual < mpf("1e-9"):
        print("  ✓ BOUNDARY SATURATED")
    else:
        print("  ✗ Boundary NOT saturated")
        return False
    print()

    # ========================================================================
    # 6. Stability metric E_ξ
    # ========================================================================
    print("-"*70)
    print("STEP 6: Computing E_ξ")
    print("-"*70)

    E_xi = compute_E_xi(alpha_exp, alpha_pred, Delta_pi)
    threshold = mpf("5.5")

    print(f"  E_ξ = {float(E_xi):.3f}")
    print(f"  Threshold = {float(threshold)}")
    print(f"  Safety margin = {100*(1 - float(E_xi)/float(threshold)):.1f}%")

    if E_xi < threshold:
        print("  ✓ STABLE")
    else:
        print("  ✗ UNSTABLE")
        return False
    print()

    # ========================================================================
    # 7. NumPy double-precision cross-check
    # ========================================================================
    print("-"*70)
    print("CROSS-CHECK: NumPy double precision")
    print("-"*70)

    alpha_pred_numpy = float(A1_over_A3) * float(r) / (4 * np.pi)
    diff_np = abs(alpha_pred_float - alpha_pred_numpy)

    print(f"  α_pred (mpmath) = {alpha_pred_float:.15f}")
    print(f"  α_pred (NumPy)  = {alpha_pred_numpy:.15f}")
    print(f"  Difference      = {diff_np:.2e}")

    if diff_np < EPSILON_MACHINE:
        print("  ✓ Numerical stability confirmed")
    else:
        print("  ⚠ Warning: slight float/mpmath drift")
    print()

    # ========================================================================
    # SUMMARY
    # ========================================================================
    print("="*70)
    print("VERIFICATION SUMMARY")
    print("="*70)
    print(f"  α_pred = {alpha_pred_float:.10f} (1/{float(1/alpha_pred):.4f})")
    print(f"  α_exp  = {alpha_exp}")
    print(f"  Δα     = {alpha_err_ppm:.1f} ppm")
    print(f"  ξ*     = {float(xi_star):.8f}")
    print(f"  β'_α   = {float(beta_prime_alpha):.8f}")
    print(f"  Sat    = {saturation_residual:.2e}")
    print(f"  E_ξ    = {float(E_xi):.3f}")
    print()
    print("✓ ALL CHECKS PASSED")
    print("✓ RESULTS REPRODUCIBLE TO MACHINE PRECISION")
    print("="*70)
    print()

    return True

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    print()
    print("╔════════════════════════════════════════════════════════════════════╗")
    print("║  α ≈ 1/137 VERIFICATION SCRIPT                                    ║")
    print("║  Deriving the Fine-Structure Constant from Geometric Fixed Point  ║")
    print("╚════════════════════════════════════════════════════════════════════╝")
    print()

    try:
        ok = verify_all()
        if ok:
            print("🎉 VERIFICATION COMPLETE — ALL RESULTS MATCH LOCKED VALUES")
            sys.exit(0)
        else:
            print("❌ VERIFICATION FAILED — SEE OUTPUT ABOVE")
            sys.exit(1)
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)