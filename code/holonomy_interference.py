"""
holonomy_interference.py
------------------------
Computational demonstration of Geometric Interference and the
Dissipative Aharonov-Bohm-type Effect (Section 5 of the paper).

NOTE: The term "Aharonov-Bohm-type" is used in the sense of curvature-
induced phase interference without Hilbert-space structure. This is a
geometric analogue of the AB effect, not the original quantum phenomenon.

Key formula (Theorem 5.6):
  Hol(γ) = exp(-Σ(γ)) · exp(-i·Φ(γ))

  For two cycles γ1, γ2 with Σ(γ1) = Σ(γ2) = Σ* but Φ(γ1) ≠ Φ(γ2):

  |Hol(γ1) + Hol(γ2)|² = 2·exp(-2Σ*)·(1 + cos(ΔΦ))

  where ΔΦ = Φ(γ1) - Φ(γ2).

The interference pattern is purely geometric (curvature-induced phase),
independent of Hilbert-space structure.

Demonstrations
--------------
1. Interference amplitude vs phase difference ΔΦ for several Σ* values.
2. Complex holonomy trajectories in the Argand plane.
3. Dependence on the local-global factorization (Euler product magnitude).
4. Phase portrait: how |Hol|² varies over the (Σ*, ΔΦ) parameter space.

Output: holonomy_interference.png saved to the same directory as this script.
"""

from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.colors import Normalize

OUTPUT_DIR = Path(__file__).parent


def holonomy(sigma: float, phi: float) -> complex:
    """Complex dissipative holonomy: Hol(γ) = exp(-Σ - i·Φ)."""
    return np.exp(-sigma) * np.exp(-1j * phi)


def interference(sigma_star: float, delta_phi: np.ndarray) -> np.ndarray:
    """
    |Hol(γ1) + Hol(γ2)|² for equal dissipation Σ* and phase difference ΔΦ.
    = 2·exp(-2Σ*)·(1 + cos(ΔΦ))
    """
    return 2 * np.exp(-2 * sigma_star) * (1 + np.cos(delta_phi))


def make_figure():
    delta_phi = np.linspace(-2 * np.pi, 2 * np.pi, 800)

    sigma_values = [0.0, 0.3, 0.6, 1.0, 1.5]
    palette = cm.viridis(np.linspace(0.1, 0.9, len(sigma_values)))

    fig, axes = plt.subplots(2, 2, figsize=(13, 11))
    fig.patch.set_facecolor("#f8f9fa")
    fig.suptitle(
        r"Geometric Interference — Aharonov–Bohm-like Phase Effect" "\n"
        r"$|\mathrm{Hol}(\gamma_1)+\mathrm{Hol}(\gamma_2)|^2"
        r"= 2\,e^{-2\Sigma^*}(1+\cos\Delta\Phi)$",
        fontsize=13, fontweight="bold",
    )

    # ── Panel 1 · Interference amplitude vs ΔΦ ────────────────────────────
    ax = axes[0, 0]
    ax.set_facecolor("#f4f4f4")
    for sig, col in zip(sigma_values, palette):
        amp = interference(sig, delta_phi)
        ax.plot(delta_phi / np.pi, amp,
                color=col, lw=2,
                label=rf"$\Sigma^* = {sig:.1f}$  "
                      rf"  $2e^{{-2\cdot{sig:.1f}}}={2*np.exp(-2*sig):.3f}$")

    ax.axhline(0, color="black", lw=0.8, ls="--", alpha=0.5)
    ax.set_xlabel(r"$\Delta\Phi / \pi$", fontsize=11)
    ax.set_ylabel(
        r"$|\mathrm{Hol}(\gamma_1)+\mathrm{Hol}(\gamma_2)|^2$", fontsize=10
    )
    ax.set_title(
        "Interference Amplitude vs Phase Difference\n"
        r"(Dissipative $\Sigma^*$ controls the envelope)",
        fontsize=11,
    )
    ax.set_xticks([-2, -1, 0, 1, 2])
    ax.set_xticklabels([r"$-2\pi$", r"$-\pi$", r"$0$", r"$\pi$", r"$2\pi$"])
    ax.legend(fontsize=8, framealpha=0.85)
    ax.grid(True, alpha=0.25)

    # ── Panel 2 · Argand plane: holonomy locus ─────────────────────────────
    ax = axes[0, 1]
    ax.set_facecolor("#f4f4f4")
    ax.set_aspect("equal")

    phi_sweep = np.linspace(0, 2 * np.pi, 500)
    for sig, col in zip(sigma_values, palette):
        H = holonomy(sig, phi_sweep)
        ax.plot(H.real, H.imag, color=col, lw=2,
                label=rf"$\Sigma^* = {sig:.1f}$,  $r = e^{{-{sig:.1f}}} = {np.exp(-sig):.3f}$")
        # Mark Φ = 0
        H0 = holonomy(sig, 0.0)
        ax.scatter([H0.real], [H0.imag], color=col, s=40, zorder=5)

    ax.axhline(0, color="black", lw=0.5, alpha=0.4)
    ax.axvline(0, color="black", lw=0.5, alpha=0.4)
    ax.scatter([0], [0], c="black", s=30, zorder=6, label="Origin")
    ax.set_xlabel(r"$\mathrm{Re}\,\mathrm{Hol}(\gamma)$", fontsize=11)
    ax.set_ylabel(r"$\mathrm{Im}\,\mathrm{Hol}(\gamma)$", fontsize=11)
    ax.set_title(
        r"Holonomy Locus in $\mathbb{C}$  (Argand Plane)" "\n"
        r"$|\mathrm{Hol}| = e^{-\Sigma^*}$,  phase $= -\Phi$",
        fontsize=11,
    )
    ax.legend(fontsize=7.5, framealpha=0.85)
    ax.grid(True, alpha=0.25)

    # ── Panel 3 · Euler factorization of magnitude ─────────────────────────
    # W(f) = Π_p exp(-Σ_p(f))
    # Demonstrate with 2 local sectors p1, p2
    ax = axes[1, 0]
    ax.set_facecolor("#f4f4f4")

    # Two cycles: σ* = 0.6, decomposed into local sectors
    n_sectors = np.arange(1, 9)
    sigma_star_ref = 0.8

    euler_product = np.zeros(len(n_sectors))
    for i, n in enumerate(n_sectors):
        # Uniform decomposition: Σ_p = Σ* / n for each of n sectors
        sigma_p = sigma_star_ref / n
        W_product = np.prod([np.exp(-sigma_p)] * n)
        euler_product[i] = W_product

    global_weight = np.exp(-sigma_star_ref)
    ax.axhline(global_weight, color="red", lw=2, ls="--",
               label=rf"Global: $e^{{-\Sigma^*}} = {global_weight:.4f}$")
    ax.plot(n_sectors, euler_product, "o-", color="#3a86ff", lw=2, ms=8,
            label=r"Euler product: $\prod_p e^{-\Sigma_p(\gamma)}$")

    ax.set_xlabel("Number of local dissipative sectors $|P|$", fontsize=11)
    ax.set_ylabel(r"$W(\gamma) = \prod_p W_p(\gamma)$", fontsize=11)
    ax.set_title(
        "Euler Product Factorization of Holonomy Magnitude\n"
        rf"($\Sigma^* = {sigma_star_ref}$, uniform sector decomposition)",
        fontsize=11,
    )
    ax.legend(fontsize=9, framealpha=0.85)
    ax.set_xticks(n_sectors)
    ax.grid(True, alpha=0.25)
    ax.text(
        5, global_weight + 0.01,
        r"Factorization is exact: $\prod_p W_p = e^{-\Sigma^*}$  $\forall\,|P|$",
        fontsize=8, color="darkred",
    )

    # ── Panel 4 · Phase portrait: |Ψ|² over (Σ*, ΔΦ) ─────────────────────
    ax = axes[1, 1]
    sigma_grid = np.linspace(0, 2.0, 200)
    dphi_grid = np.linspace(-np.pi, np.pi, 200)
    SG, DP = np.meshgrid(sigma_grid, dphi_grid)
    AMP = 2 * np.exp(-2 * SG) * (1 + np.cos(DP))

    im = ax.pcolormesh(SG, DP / np.pi, AMP,
                       cmap="inferno", shading="auto")
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label(r"$|\Psi_{\mathrm{total}}|^2$", fontsize=10)

    # Mark constructive/destructive lines
    ax.axhline(0, color="white", lw=1.2, ls="--", alpha=0.8,
               label=r"$\Delta\Phi=0$ (constructive)")
    ax.axhline(1, color="cyan", lw=1.2, ls="--", alpha=0.8,
               label=r"$\Delta\Phi=\pi$ (destructive)")
    ax.axhline(-1, color="cyan", lw=1.2, ls="--", alpha=0.8)

    ax.set_xlabel(r"$\Sigma^*$ (dissipative cost)", fontsize=11)
    ax.set_ylabel(r"$\Delta\Phi / \pi$", fontsize=11)
    ax.set_title(
        r"Phase Portrait: $|\Psi|^2$ over $(\Sigma^*, \Delta\Phi)$" "\n"
        r"Dissipation damps the envelope; phase controls fringes",
        fontsize=11,
    )
    ax.legend(fontsize=8, loc="upper right", framealpha=0.75)

    plt.tight_layout(rect=[0, 0, 1, 0.93])

    out_path = OUTPUT_DIR / "holonomy_interference.png"
    plt.savefig(out_path, dpi=180, bbox_inches="tight")
    print(f"Saved: {out_path}")
    plt.close()


if __name__ == "__main__":
    make_figure()
