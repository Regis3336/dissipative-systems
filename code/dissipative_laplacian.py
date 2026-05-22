"""
dissipative_laplacian.py
------------------------
Computational demonstration of Instantaneous Markov Kernels and the
Dissipative Laplacian (Section 6 of the paper).

Given a small dissipative category modeled as a directed weighted graph:

  P_t(X → Y) = exp(-d_JS(X,Y; W_t)) / Σ_Z exp(-d_JS(X,Z; W_t))

  Δ_t = -dP_t/dt   (dissipative Laplacian)

  (Δ_t φ)(X) = Σ_Y Ṗ_t(X→Y) · (φ(Y) - φ(X))

Key result visualized:
  Δ_t(f,g) ∝ (Ric_JS^Fil(f,W_t) - Ric_JS^Fil(g,W_t)) · P_t(f→g)
  => curvature differences create anisotropic diffusion gradients.

Also demonstrates the non-semigroup property:
  P_{t+s} ≠ P_t · P_s
  because P_t is an INSTANTANEOUS GEOMETRIC PROBE, not a Markov propagator.
  The non-semigroup deviation arises from the time-dependence of the probe
  itself, not from a categorical constraint invoked directly.

SCOPE NOTE
----------
This demo models the instantaneous-kernel layer on a finite directed
weighted skeleton. The matrix SIGMA[i,j] is assigned directly and is NOT
intended to verify categorical composition additivity Σ(g∘f) = Σ(g) + Σ(f).
For a composition-additive realization, replace SIGMA[i,j] with a potential
difference E(j) - E(i) for a fixed energy function E on the nodes.

Demonstrations
--------------
1. Instantaneous kernel P_t as a heatmap at t=0, 0.5, 1.5.
2. Dissipative Laplacian Δ_t vs time for selected node pairs.
3. Non-semigroup check: ||P_{t+s} - P_t·P_s||_F vs t.
4. Natural weights W_0 and perturbation stability.

Output: dissipative_laplacian.png saved to the same directory as this script.
"""

from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.colors import Normalize
from scipy.special import rel_entr

OUTPUT_DIR = Path(__file__).parent

# ── Small dissipative category (directed graph, 6 nodes) ─────────────────────
N = 6  # nodes: X_0, ..., X_5
NODES = [f"$X_{i}$" for i in range(N)]

# Dissipative functional Σ: encoded as weight matrix Σ[i,j] for morphism i→j
# 0 on diagonal (identity), positive off-diagonal
RNG = np.random.default_rng(0)
SIGMA = np.zeros((N, N))
for i in range(N):
    for j in range(N):
        if i != j:
            SIGMA[i, j] = 0.2 + 0.8 * RNG.random()

# Curvature values Ric_JS^Fil assigned to each edge (i,j)
RIC = np.zeros((N, N))
for i in range(N):
    for j in range(N):
        if i != j:
            RIC[i, j] = 1.5 * (RNG.random() - 0.5)  # in [-0.75, 0.75]


def weight_matrix(t: float) -> np.ndarray:
    """W_t[i,j] = exp(-Σ[i,j] - Ric[i,j]*t) for i≠j, 1 on diagonal."""
    W = np.exp(-SIGMA - RIC * t)
    np.fill_diagonal(W, 1.0)
    return W


def js_divergence(p: np.ndarray, q: np.ndarray, eps: float = 1e-12) -> float:
    """Jensen-Shannon divergence between normalized distributions p and q."""
    p = p + eps
    q = q + eps
    p /= p.sum()
    q /= q.sum()
    m = 0.5 * (p + q)
    return 0.5 * (np.sum(rel_entr(p, m)) + np.sum(rel_entr(q, m)))


def markov_kernel(t: float) -> np.ndarray:
    """
    Instantaneous Markov kernel P_t based on JS-distance between
    row distributions of W_t.

    P_t[i,j] = exp(-d_JS(row_i, row_j; W_t)) / Σ_k exp(-d_JS(row_i, row_k; W_t))
    """
    W = weight_matrix(t)
    # Row distributions (outgoing weight profiles)
    row_sums = W.sum(axis=1, keepdims=True)
    P_rows = W / row_sums  # shape (N, N): P_rows[i] is distribution of morphisms from i

    P_kernel = np.zeros((N, N))
    for i in range(N):
        log_weights = np.zeros(N)
        for j in range(N):
            d = js_divergence(P_rows[i].copy(), P_rows[j].copy())
            log_weights[j] = -d
        log_weights -= log_weights.max()  # numerical stability
        weights = np.exp(log_weights)
        P_kernel[i] = weights / weights.sum()

    return P_kernel


def dissipative_laplacian(t: float, dt: float = 1e-4) -> np.ndarray:
    """Δ_t ≈ -(P_{t+dt} - P_{t-dt}) / (2*dt)."""
    P_fwd = markov_kernel(t + dt)
    P_bwd = markov_kernel(t - dt) if t >= dt else markov_kernel(dt)
    return -(P_fwd - P_bwd) / (2 * dt)


def make_figure():
    t_snapshots = [0.0, 0.5, 1.5]
    t_series = np.linspace(0.01, 3.0, 60)

    print("Computing Markov kernels...")
    kernels = {t: markov_kernel(t) for t in t_snapshots}

    print("Computing Laplacian time series...")
    lap_01 = [dissipative_laplacian(t)[0, 1] for t in t_series]
    lap_23 = [dissipative_laplacian(t)[2, 3] for t in t_series]
    lap_45 = [dissipative_laplacian(t)[4, 5] for t in t_series]

    print("Computing non-semigroup deviation...")
    s_fixed = 0.5
    semigroup_err = []
    for t in t_series:
        Pt = markov_kernel(t)
        Ps = markov_kernel(s_fixed)
        Pts = markov_kernel(t + s_fixed)
        semigroup_err.append(np.linalg.norm(Pts - Pt @ Ps, "fro"))

    print("Computing weight perturbation stability...")
    sigma_ref = SIGMA[0, 1]
    delta_range = np.linspace(-0.5, 0.5, 200)
    W0_ref = np.exp(-sigma_ref)
    W0_perturbed = np.exp(-(sigma_ref + delta_range))

    # ── Figure ──────────────────────────────────────────────────────────────
    fig, axes = plt.subplots(2, 2, figsize=(14, 11))
    fig.patch.set_facecolor("#f8f9fa")
    fig.suptitle(
        "Instantaneous Markov Kernels & Dissipative Laplacian  (Section 6)",
        fontsize=13, fontweight="bold",
    )

    # ── Panel 1 · Kernel heatmaps at t=0, 0.5, 1.5 ────────────────────────
    ax = axes[0, 0]
    # Stack 3 kernels side-by-side into one elongated heatmap
    combined = np.hstack([kernels[t] for t in t_snapshots])
    vmin, vmax = combined.min(), combined.max()
    im = ax.imshow(combined, aspect="auto", cmap="YlOrRd",
                   vmin=vmin, vmax=vmax)
    plt.colorbar(im, ax=ax, label=r"$P_t(X_i \to X_j)$")

    # Vertical dividers
    for k in range(1, len(t_snapshots)):
        ax.axvline(k * N - 0.5, color="black", lw=2)

    # Y-axis labels
    ax.set_yticks(range(N))
    ax.set_yticklabels(NODES, fontsize=9)
    ax.set_ylabel("Source node $X_i$", fontsize=10)

    # X-axis: group ticks per snapshot
    xtick_pos = [N // 2 + k * N for k in range(len(t_snapshots))]
    ax.set_xticks(xtick_pos)
    ax.set_xticklabels([f"$t = {t}$" for t in t_snapshots], fontsize=9)
    ax.set_title(
        r"Instantaneous Markov Kernel $P_t$ at $t = 0,\,0.5,\,1.5$" "\n"
        r"($P_t$ is a geometric probe, not a propagator: $P_{t+s} \neq P_t P_s$)",
        fontsize=11,
    )

    # ── Panel 2 · Laplacian Δ_t time series ───────────────────────────────
    ax = axes[0, 1]
    ax.set_facecolor("#f4f4f4")
    ax.plot(t_series, lap_01, color="#e63946", lw=2,
            label=r"$\Delta_t(X_0 \to X_1)$")
    ax.plot(t_series, lap_23, color="#3a86ff", lw=2,
            label=r"$\Delta_t(X_2 \to X_3)$")
    ax.plot(t_series, lap_45, color="#2a9d8f", lw=2,
            label=r"$\Delta_t(X_4 \to X_5)$")
    ax.axhline(0, color="gray", lw=0.8, ls="--", alpha=0.5)
    ax.set_xlabel(r"Time $t$", fontsize=11)
    ax.set_ylabel(r"$(\Delta_t)_{ij} = -\dot{P}_t(X_i \to X_j)$", fontsize=10)
    ax.set_title(
        r"Dissipative Laplacian $\Delta_t = -\dot{P}_t$" "\n"
        "Selected edge components vs time",
        fontsize=11,
    )
    ax.legend(fontsize=9, framealpha=0.85)
    ax.grid(True, alpha=0.25)

    # ── Panel 3 · Non-semigroup deviation ─────────────────────────────────
    ax = axes[1, 0]
    ax.set_facecolor("#f4f4f4")
    ax.semilogy(t_series, semigroup_err, color="#6a0dad", lw=2.5)
    ax.set_xlabel(r"Time $t$", fontsize=11)
    ax.set_ylabel(r"$\|P_{t+s} - P_t P_s\|_F$  (log scale)", fontsize=10)
    ax.set_title(
        rf"Non-Semigroup Deviation  ($s = {s_fixed}$ fixed)" "\n"
        r"$P_{t+s} \neq P_t P_s$: $P_t$ is a geometric probe, not a Markov propagator",
        fontsize=11,
    )
    ax.grid(True, which="both", alpha=0.25)
    ax.axhline(1e-10, color="gray", ls="--", lw=0.8, alpha=0.5)

    # ── Panel 4 · Natural weight stability under perturbation of Σ ─────────
    ax = axes[1, 1]
    ax.set_facecolor("#f4f4f4")
    ax.plot(delta_range, W0_perturbed, color="#e63946", lw=2.5,
            label=r"$W_0(\Sigma^* + \delta) = e^{-(\Sigma^*+\delta)}$")
    ax.axvline(0, color="black", lw=0.8, ls="--", alpha=0.5)
    ax.axhline(W0_ref, color="navy", lw=1.5, ls=":",
               label=rf"Reference $W_0 = e^{{-\Sigma^*}} = {W0_ref:.4f}$")

    # Shade ±0.1 stability band
    band = 0.1
    dw_band = np.exp(-(sigma_ref + np.array([-band, band])))
    ax.fill_between(
        delta_range,
        np.exp(-(sigma_ref + delta_range)) * 0,
        W0_perturbed,
        where=(np.abs(delta_range) <= band),
        alpha=0.15, color="green", label=rf"$|\delta| \leq {band}$ band",
    )
    ax.set_xlabel(r"Perturbation $\delta$ of $\Sigma$", fontsize=11)
    ax.set_ylabel(r"$W_0(\Sigma^*+\delta) = e^{-(\Sigma^*+\delta)}$", fontsize=10)
    ax.set_title(
        r"Natural Weight Stability under $\Sigma$ Perturbation" "\n"
        r"$W_0$ is $C^\infty$ and strictly monotone in $\Sigma$",
        fontsize=11,
    )
    ax.legend(fontsize=9, framealpha=0.85)
    ax.grid(True, alpha=0.25)

    # Annotate slope = -W0
    ax.annotate(
        r"Slope $= -W_0$ (stable, smooth)",
        xy=(0.05, W0_ref * np.exp(-0.05)),
        xytext=(0.2, W0_ref + 0.05),
        arrowprops=dict(arrowstyle="->", color="gray"),
        fontsize=8,
    )

    plt.tight_layout(rect=[0, 0, 1, 0.95])

    out_path = OUTPUT_DIR / "dissipative_laplacian.png"
    plt.savefig(out_path, dpi=180, bbox_inches="tight")
    print(f"Saved: {out_path}")
    plt.close()


if __name__ == "__main__":
    make_figure()
