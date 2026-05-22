"""
filippov_ricci_flow.py
----------------------
Computational illustration of the a.e. branch of the Filippov-Ricci
Dissipative Flow (Section 4 of the paper).

This is a FINITE SELECTED-CURVATURE REALIZATION of the Filippov-Ricci
inclusion, not a full multivalued/set-valued simulation. Curvature values
Ric_JS^Fil(f_i) are assigned explicitly; the script illustrates the a.e.-
unique ODE branch that arises from a fixed measurable selection.

Demonstrates:
  1. Curvature Amplification Theorem (Thm 4.5):
     W_t(f) / W_t(g) → 0 or ∞ depending on Ric_JS^Fil(f) vs Ric_JS^Fil(g).

  2. Exponential separation of weight trajectories for morphisms with
     distinct regularized curvature values.

  3. Weight landscape deformation over time at fixed Σ.

NOTE on normalization
---------------------
The evolving quantities W_t(f) are UNNORMALIZED DYNAMIC INTENSITIES.
Only W_0 = exp(-Σ) is the canonical dissipative attenuation factor.
When W_t > 1 (negative curvature), this reflects intensification of the
dissipative probe, not a violation of the attenuation principle.
When a probabilistic interpretation is needed, W_t is always normalized
into the instantaneous Markov kernel P_t (see dissipative_laplacian.py).

Model
-----
  W_0(f_i) = exp(-Σ(f_i))                         [static potential]
  Ẇ_t(f_i) = -Ric_i * W_t(f_i)                   [a.e. Filippov branch]
  => W_t(f_i) = exp(-Σ(f_i) - Ric_i * t)

Output: filippov_ricci_flow.png saved to the same directory as this script.
"""

from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm

OUTPUT_DIR = Path(__file__).parent

# ── Synthetic dissipative category ───────────────────────────────────────────
# We define a small category with 5 morphisms having different (Σ, Ric) pairs.

RNG = np.random.default_rng(42)

MORPHISMS = [
    # (label,  Sigma,  Ric_JS_Fil)
    (r"$f_1$: high $\kappa$, low $\Sigma$",   0.30,  2.50),
    (r"$f_2$: low $\kappa$, low $\Sigma$",    0.35, -0.50),
    (r"$f_3$: high $\kappa$, high $\Sigma$",  1.20,  2.00),
    (r"$f_4$: zero $\kappa$, mid $\Sigma$",   0.80,  0.00),
    (r"$f_5$: neg $\kappa$, mid $\Sigma$",    0.75, -1.80),
    (r"$f_6$: moderate $\kappa$",             0.50,  0.85),
]


def weight(t: np.ndarray, sigma: float, ric: float) -> np.ndarray:
    """Filippov weight trajectory: W_t = exp(-Σ - Ric * t)."""
    return np.exp(-sigma - ric * t)


def weight_ratio(t: np.ndarray, m1, m2) -> np.ndarray:
    """
    W_t(f_i) / W_t(f_j) = exp(-(Ric_i - Ric_j)*t - (Σ_i - Σ_j))
    """
    _, sig_i, ric_i = m1
    _, sig_j, ric_j = m2
    return np.exp(-(ric_i - ric_j) * t - (sig_i - sig_j))


def make_figure():
    t = np.linspace(0, 4.0, 500)
    palette = cm.tab10(np.linspace(0, 0.9, len(MORPHISMS)))

    fig, axes = plt.subplots(1, 3, figsize=(15, 5.5))
    fig.patch.set_facecolor("#f8f9fa")
    fig.suptitle(
        "Filippov–Ricci Flow: a.e. Selected-Curvature Realization"
        "  —  Curvature Amplification Theorem",
        fontsize=13, fontweight="bold",
    )

    # ── Panel 1 · Weight trajectories W_t(f) ─────────────────────────────
    ax = axes[0]
    ax.set_facecolor("#f4f4f4")
    for (label, sig, ric), col in zip(MORPHISMS, palette):
        W = weight(t, sig, ric)
        ax.plot(t, W, label=label, color=col, lw=2)

    ax.set_xlabel(r"Time $t$", fontsize=11)
    ax.set_ylabel(r"$W_t(f) = e^{-\Sigma(f) - \mathrm{Ric}(f)\,t}$", fontsize=10)
    ax.set_title(
        "Unnormalized Dynamic Intensities $W_t$\n"
        r"(a.e. branch; normalize into $P_t$ for probabilities)",
        fontsize=11,
    )
    ax.set_ylim(bottom=0)
    ax.legend(fontsize=7.5, loc="upper right", framealpha=0.85)
    ax.grid(True, alpha=0.25)
    ax.annotate(
        r"Low $\kappa$ dominates for $t\to\infty$",
        xy=(3.8, weight(np.array([3.8]), *MORPHISMS[1][1:])[0]),
        xytext=(2.5, 1.3),
        arrowprops=dict(arrowstyle="->", color="black", lw=1),
        fontsize=8,
    )

    # ── Panel 2 · Weight ratios (curvature amplification) ─────────────────
    ax = axes[1]
    ax.set_facecolor("#f4f4f4")

    # f1 vs f2: large Ric difference — exponential separation
    r12 = weight_ratio(t, MORPHISMS[0], MORPHISMS[1])
    ax.semilogy(t, r12, color=palette[0], lw=2.5,
                label=rf"$W_t(f_1)/W_t(f_2)$  "
                      rf"$\Delta\kappa={MORPHISMS[0][2]-MORPHISMS[1][2]:+.2f}$")

    # f2 vs f1: inverse
    ax.semilogy(t, 1.0 / r12, color=palette[1], lw=2.5, ls="--",
                label=rf"$W_t(f_2)/W_t(f_1)$  "
                      rf"$\Delta\kappa={MORPHISMS[1][2]-MORPHISMS[0][2]:+.2f}$")

    # f5 vs f4: negative vs zero curvature
    r54 = weight_ratio(t, MORPHISMS[4], MORPHISMS[3])
    ax.semilogy(t, r54, color=palette[4], lw=2.5, ls="-.",
                label=rf"$W_t(f_5)/W_t(f_4)$  "
                      rf"$\Delta\kappa={MORPHISMS[4][2]-MORPHISMS[3][2]:+.2f}$")

    # Zero-curvature reference
    ax.axhline(1, color="gray", lw=1, ls=":", alpha=0.6, label="Ratio = 1 (equal curvature)")

    ax.set_xlabel(r"Time $t$", fontsize=11)
    ax.set_ylabel(r"$W_t(f_i) / W_t(f_j)$   (log scale)", fontsize=10)
    ax.set_title(
        "Curvature Amplification (Thm 4.5)\n"
        r"$W_t(f)/W_t(g) = \exp(-\Delta\kappa\cdot t - \Delta\Sigma)$",
        fontsize=11,
    )
    ax.legend(fontsize=7.5, framealpha=0.85)
    ax.grid(True, which="both", alpha=0.25)

    # ── Panel 3 · Weight landscape at several times ────────────────────────
    ax = axes[2]
    ax.set_facecolor("#f4f4f4")

    ric_sweep = np.linspace(-3, 3, 300)
    sigma_ref = 0.6
    t_snapshots = [0.0, 0.5, 1.0, 2.0, 4.0]
    snap_colors = cm.plasma(np.linspace(0.1, 0.85, len(t_snapshots)))

    for t_snap, col in zip(t_snapshots, snap_colors):
        W_snap = np.exp(-sigma_ref - ric_sweep * t_snap)
        ax.plot(ric_sweep, W_snap, color=col, lw=2,
                label=rf"$t = {t_snap:.1f}$")

    ax.axvline(0, color="black", lw=0.8, ls="--", alpha=0.5)
    ax.set_xlabel(r"$\mathrm{Ric}_{\mathrm{JS}}^{\mathrm{Fil}}(f)$", fontsize=11)
    ax.set_ylabel(r"$W_t(f)$", fontsize=11)
    ax.set_title(
        r"Weight Landscape vs Curvature at $t = 0, 0.5, 1, 2, 4$" "\n"
        r"($\Sigma = 0.6$ fixed for all morphisms)",
        fontsize=11,
    )
    ax.set_ylim(bottom=0, top=None)
    ax.legend(fontsize=9, framealpha=0.85, title="Time snapshot")
    ax.grid(True, alpha=0.25)
    ax.annotate(
        r"High $\kappa$ → $W_t\to 0$",
        xy=(2.5, np.exp(-sigma_ref - 2.5 * 1.0)),
        xytext=(1.2, 0.8),
        arrowprops=dict(arrowstyle="->", color="gray"),
        fontsize=8,
    )
    ax.annotate(
        r"Low $\kappa$ → $W_t\to\infty$",
        xy=(-2.5, np.exp(-sigma_ref - (-2.5) * 1.0)),
        xytext=(-2.8, 1.8),
        arrowprops=dict(arrowstyle="->", color="gray"),
        fontsize=8,
    )

    plt.tight_layout(rect=[0, 0, 1, 0.95])

    out_path = OUTPUT_DIR / "filippov_ricci_flow.png"
    plt.savefig(out_path, dpi=180, bbox_inches="tight")
    print(f"Saved: {out_path}")
    plt.close()


if __name__ == "__main__":
    make_figure()
