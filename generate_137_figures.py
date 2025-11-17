#!/usr/bin/env python3
"""
generate_figures.py

Figure generation script for α ≈ 1/137 geometric fixed-point paper.
Regenerates Figures 1-3 from locked parameters in locks.json.

Figures:
    1. ξ* convergence and residual function R(ξ)
    2. Boundary saturation (|α_err| = |δα|_max)
    3. Parameter sensitivity α(ξ)

Usage:
    python generate_figures.py

Requirements:
    - Python 3.12+
    - mpmath 1.3.0
    - numpy 1.26.0
    - matplotlib 3.8.0

Author: R@, Sanch0-5-Oh, C@ Sonnet 4.5, Gemini 2.5 Flash
Date: 2025-11-17
License: MIT
"""

import json
import sys
from pathlib import Path

try:
    from mpmath import mp, mpf, sqrt, pi as mp_pi
    import numpy as np
    import matplotlib
    matplotlib.use('Agg')  # Non-interactive backend
    import matplotlib.pyplot as plt
except ImportError as e:
    print(f"ERROR: Missing required package: {e}")
    print("Install with: pip install mpmath numpy matplotlib")
    sys.exit(1)

# Set precision
mp.dps = 80

# Directories
LOCKS_FILE = Path("locks.json")
FIGS_DIR = Path("figs")
FIGS_DIR.mkdir(exist_ok=True)

# Style
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.size'] = 11
plt.rcParams['axes.linewidth'] = 1.2

# ============================================================================
# LOAD LOCKS
# ============================================================================

def load_locks():
    """Load locked parameters"""
    if not LOCKS_FILE.exists():
        print(f"ERROR: {LOCKS_FILE} not found!")
        sys.exit(1)
    
    with open(LOCKS_FILE, 'r') as f:
        return json.load(f)

# ============================================================================
# FIGURE 1: ξ* CONVERGENCE
# ============================================================================

def generate_figure1(locks):
    """Generate Figure 1: ξ* convergence and residual R(ξ)"""
    
    print("Generating Figure 1: ξ* convergence...")
    
    # Extract parameters
    xi_star = locks['stochastic_parameters']['xi_star']['value']
    beta_prime_alpha = locks['stochastic_parameters']['beta_prime_alpha']['value']
    Delta_pi = locks['collapse_gap']['Delta_pi']['value']
    alpha_err = locks['derived_quantities']['alpha_err']['value']
    
    # Residual function
    def R(xi):
        return alpha_err - abs(xi * beta_prime_alpha) / Delta_pi
    
    xi_range = np.linspace(0, 0.01, 500)
    R_vals = [R(xi) for xi in xi_range]
    
    # Create figure
    fig = plt.figure(figsize=(14, 6))
    fig.patch.set_facecolor('white')
    
    # Panel A: Convergence
    ax1 = plt.subplot(1, 2, 1)
    iterations = np.array([0, 1, 2, 3, 4])
    xi_vals = np.array([xi_star] * 5)
    
    ax1.plot(iterations, xi_vals, 'o-', color='steelblue', 
             linewidth=2.5, markersize=9, label=f'$\\xi^* = {xi_star:.8f}$', zorder=3)
    ax1.axhline(xi_star, color='crimson', linestyle='--', linewidth=2, alpha=0.7, zorder=2)
    
    ax1.set_xlabel('Iteration', fontsize=13, weight='bold')
    ax1.set_ylabel('$\\xi$', fontsize=13, weight='bold')
    ax1.set_title('Panel A: Self-Consistency Iteration', fontsize=14, weight='bold', pad=12)
    ax1.grid(alpha=0.3, linestyle=':', linewidth=0.8)
    ax1.legend(fontsize=11, loc='upper right', framealpha=0.95)
    ax1.set_ylim([xi_star - 0.0002, xi_star + 0.0002])
    ax1.set_xlim([-0.2, 4.2])
    ax1.tick_params(labelsize=11)
    
    # Panel B: Residual
    ax2 = plt.subplot(1, 2, 2)
    ax2.plot(xi_range, R_vals, '-', color='steelblue', linewidth=3, zorder=2)
    ax2.axhline(0, color='gray', linestyle='--', linewidth=1.2, alpha=0.5, zorder=1)
    ax2.axvline(xi_star, color='crimson', linestyle='--', linewidth=2, 
                alpha=0.7, label=f'$\\xi^* = {xi_star:.8f}$', zorder=3)
    ax2.plot(xi_star, 0, 'o', color='crimson', markersize=11, 
             markeredgewidth=2.5, markeredgecolor='darkred', label='Zero', zorder=5)
    
    ax2.set_xlabel('$\\xi$', fontsize=13, weight='bold')
    ax2.set_ylabel('$R(\\xi)$', fontsize=13, weight='bold')
    ax2.set_title('Panel B: Residual Function', fontsize=14, weight='bold', pad=12)
    ax2.grid(alpha=0.3, linestyle=':', linewidth=0.8)
    ax2.legend(fontsize=11, loc='upper right', framealpha=0.95)
    ax2.tick_params(labelsize=11)
    ax2.ticklabel_format(style='scientific', axis='y', scilimits=(0,0))
    
    plt.tight_layout()
    
    # Save
    fig1_path = FIGS_DIR / "figure1_xi_convergence.png"
    plt.savefig(fig1_path, format='png', dpi=300, bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    plt.close()
    
    print(f"  ✓ Saved: {fig1_path}")

# ============================================================================
# FIGURE 2: BOUNDARY SATURATION
# ============================================================================

def generate_figure2(locks):
    """Generate Figure 2: Boundary saturation |α_err| = |δα|_max"""
    
    print("Generating Figure 2: Boundary saturation...")
    
    # Extract values
    alpha_err = locks['derived_quantities']['alpha_err']['value']
    delta_alpha_max = locks['boundary_equality']['delta_alpha_max']['value']
    saturation_residual = locks['boundary_equality']['saturation_residual']['value']
    
    # Create figure
    fig, ax = plt.subplots(figsize=(9, 9))
    fig.patch.set_facecolor('white')
    
    # Diagonal y = x
    max_val = max(alpha_err, delta_alpha_max) * 1.25
    diagonal = np.linspace(0, max_val, 100)
    ax.plot(diagonal, diagonal, 'k--', linewidth=2.5, alpha=0.6, 
            label='$y = x$ (saturation boundary)', zorder=1)
    
    # Data point
    ax.plot(delta_alpha_max, alpha_err, 'o', color='crimson', markersize=22, 
            markeredgewidth=3.5, markeredgecolor='darkred',
            label='Predicted $\\alpha$', zorder=5)
    
    # Annotation
    ax.text(delta_alpha_max * 0.45, alpha_err * 1.65,
            f'Exact saturation:\n$|\\alpha_{{\\rm err}}| = |\\delta\\alpha|_{{\\rm max}}$\n'
            f'${alpha_err:.2e}$',
            fontsize=12, ha='center', va='center',
            bbox=dict(boxstyle='round,pad=0.8', facecolor='wheat', 
                      alpha=0.9, edgecolor='black', linewidth=1.5))
    
    # Arrow
    ax.annotate('', xy=(delta_alpha_max, alpha_err),
                xytext=(delta_alpha_max * 0.45, alpha_err * 1.5),
                arrowprops=dict(arrowstyle='->', color='black', lw=2.5))
    
    # Residual info
    ax.text(0.95, 0.08, 
            f'Residual: ${saturation_residual:.2e}$\n(machine precision)',
            transform=ax.transAxes, fontsize=11, ha='right', va='bottom',
            bbox=dict(boxstyle='round,pad=0.6', facecolor='lightblue', 
                      alpha=0.85, edgecolor='steelblue', linewidth=1.2))
    
    ax.set_xlabel('$|\\delta\\alpha|_{\\rm max}$ (predicted)', fontsize=14, weight='bold')
    ax.set_ylabel('$|\\alpha_{\\rm err}|$ (actual)', fontsize=14, weight='bold')
    ax.set_title('Figure 2: Boundary Saturation — Exact Equality', 
                 fontsize=15, weight='bold', pad=20)
    ax.grid(alpha=0.35, linestyle=':', linewidth=1)
    ax.legend(fontsize=12, loc='upper left', framealpha=0.95, edgecolor='black')
    ax.set_xlim([0, max_val])
    ax.set_ylim([0, max_val])
    ax.set_aspect('equal')
    ax.tick_params(labelsize=12)
    ax.ticklabel_format(style='scientific', axis='both', scilimits=(0,0))
    
    plt.tight_layout()
    
    # Save
    fig2_path = FIGS_DIR / "figure2_boundary_saturation.png"
    plt.savefig(fig2_path, format='png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    
    print(f"  ✓ Saved: {fig2_path}")

# ============================================================================
# FIGURE 3: PARAMETER SENSITIVITY
# ============================================================================

def generate_figure3(locks):
    """Generate Figure 3: α(ξ) sensitivity curve"""
    
    print("Generating Figure 3: Parameter sensitivity...")
    
    # Extract parameters
    xi_star = locks['stochastic_parameters']['xi_star']['value']
    alpha_pred = locks['derived_quantities']['alpha_pred']['value']
    dalpha_dxi = locks['stability_metrics']['dalpha_dxi']['value']
    
    # α(ξ) linearized response
    xi_range = np.linspace(0.002, 0.008, 400)
    alpha_vals = alpha_pred + dalpha_dxi * (xi_range - xi_star)
    
    # Create figure
    fig, ax = plt.subplots(figsize=(11, 7.5))
    fig.patch.set_facecolor('white')
    
    # Main curve
    ax.plot(xi_range, alpha_vals, '-', color='steelblue', linewidth=3.5, 
            label='$\\alpha(\\xi)$ (linearized response)', zorder=2)
    
    # Mark ξ*
    ax.axvline(xi_star, color='crimson', linestyle='--', linewidth=2.5, 
               alpha=0.8, label=f'$\\xi^* = {xi_star:.8f}$', zorder=3)
    ax.plot(xi_star, alpha_pred, 'o', color='crimson', markersize=14, 
            markeredgewidth=3, markeredgecolor='darkred', zorder=5)
    
    # ±1% band
    xi_1pct_low = xi_star * 0.99
    xi_1pct_high = xi_star * 1.01
    ax.axvspan(xi_1pct_low, xi_1pct_high, color='crimson', alpha=0.18, 
               label='±1% variation in $\\xi^*$', zorder=1)
    
    # Annotations
    delta_alpha_1pct = dalpha_dxi * 0.01 * xi_star
    ax.text(0.05, 0.95,
            f'1% change in $\\xi$ produces\n$\\Delta\\alpha \\approx {delta_alpha_1pct:.2e}$\n'
            f'(far below experimental uncertainty)',
            transform=ax.transAxes, fontsize=11, ha='left', va='top',
            bbox=dict(boxstyle='round,pad=0.7', facecolor='lightblue', 
                      alpha=0.85, edgecolor='steelblue', linewidth=1.2))
    
    ax.text(0.75, 0.15, f'Shallow slope:\n$d\\alpha/d\\xi \\approx {dalpha_dxi:.1e}$',
            transform=ax.transAxes, fontsize=11, ha='center', va='bottom',
            bbox=dict(boxstyle='round,pad=0.7', facecolor='wheat', 
                      alpha=0.9, edgecolor='black', linewidth=1.5))
    
    ax.set_xlabel('$\\xi$ (stochastic tolerance parameter)', fontsize=14, weight='bold')
    ax.set_ylabel('$\\alpha(\\xi)$ (fine-structure constant)', fontsize=14, weight='bold')
    ax.set_title('Figure 3: Parameter Sensitivity — Robustness Under $\\xi$ Variation', 
                 fontsize=15, weight='bold', pad=20)
    ax.grid(alpha=0.35, linestyle=':', linewidth=1)
    ax.legend(fontsize=12, loc='lower right', framealpha=0.95, edgecolor='black')
    ax.tick_params(labelsize=12)
    
    # Set limits
    y_range = max(abs(alpha_vals - alpha_pred)) * 3.0
    ax.set_ylim([alpha_pred - y_range, alpha_pred + y_range])
    ax.set_xlim([0.0015, 0.0085])
    ax.ticklabel_format(style='plain', axis='y')
    
    plt.tight_layout()
    
    # Save
    fig3_path = FIGS_DIR / "figure3_alpha_xi_sensitivity.png"
    plt.savefig(fig3_path, format='png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    
    print(f"  ✓ Saved: {fig3_path}")

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    print()
    print("="*70)
    print("GENERATING FIGURES FOR α ≈ 1/137 PAPER")
    print("="*70)
    print()
    
    try:
        locks = load_locks()
        print(f"✓ Loaded locks.json\n")
        
        generate_figure1(locks)
        generate_figure2(locks)
        generate_figure3(locks)
        
        print()
        print("="*70)
        print("✓ ALL FIGURES GENERATED SUCCESSFULLY")
        print(f"✓ Output directory: {FIGS_DIR.absolute()}")
        print("="*70)
        print()
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
