# Dissipative Systems: From the Second Law of Thermodynamics to Filippov–Ricci Geometry

**Author:** Reinaldo Elias de Souza Junior  
**Affiliation:** Faculdade de Medicina, Universidade Federal de Goiás, Brasil  
**Date:** May 2026

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20339888.svg)](https://doi.org/10.5281/zenodo.20339888)

---

## Abstract

We introduce a unified geometric framework for irreversible systems by equipping small categories with an additive entropy-production functional Σ : Mor(C) → ℝ≥₀. The induced natural weights W(f) = e^(−Σ(f)) behave as thermodynamically consistent attenuation factors and render the category *causally rigid*: all reversible morphisms collapse to identities.

The framework establishes three structural components:

1. **Filippov–Ricci flow**: evolution of dissipative weights under nonsmooth curvature
2. **Instantaneous Markov kernels**: geometric probes (not propagators) that produce a dissipative Laplacian Δₜ = −Ṗₜ
3. **Complex dissipative holonomy**: magnitude controlled by dissipation, phase by curvature, producing interference without Hilbert space

A central result is the emergence of an *integer-valued arithmetic invariant*: for any analytic observable L(s) with L(s) ≠ 0, the induced connection on S² has first Chern class c₁(L(s)) ∈ {−1, 0, +1}, determined by the local singularity structure of L(s).

**Core thesis:** Irreversibility does not destroy geometry — it reshapes it.

---

## Repository Structure
.
├── dissipative_systems_ricci_filippov.pdf                # Main paper (PDF source)
├── references.bib                                        # Bibliography
├── figures/
│   ├── dissipative_laplacian.png
│   ├── filippov_ricci_flow.png
│   ├── holonomy_interference.png
│   └── chern_stratification.png
└── code/
├── chern_stratification.py                                # Ternary phase index q_L ∈ {-1,0,+1}
├── dissipative_laplacian.py                               # Instantaneous kernels & Δₜ
├── filippov_ricci_flow.py                                 # Curvature amplification theorem
└── holonomy_interference.py                               # Geometric interference (AB-type)

---

## Code Validation

The computational implementations serve as **operational validation** of the theoretical framework. Each script:

- Implements formulas **exactly as stated** in the paper
- Includes scope notes and disclaimers where classical intuitions fail
- Generates figures demonstrating key theorems

**Key validated results:**
- ✓ Filippov–Ricci weight evolution: Wₜ(f) = exp(−Σ(f) − Ric(f)·t)
- ✓ Non-semigroup property: Pₜ₊ₛ ≠ Pₜ · Pₛ (geometric probe, not propagator)
- ✓ Interference formula: |Hol(γ₁) + Hol(γ₂)|² = 2e^(−2Σ*)(1 + cos ΔΦ)
- ✓ Ternary Chern classification: qₗ(s) ∈ {−1, 0, +1}

**Methodological note:** Code generation preceded mathematical auditing. This protocol prevented ontological drift — the code acts as an anchor, forcing operational fidelity to the paper's definitions rather than classical reinterpretation.

---

## Requirements

### Python Dependencies
```bash
pip install numpy matplotlib scipy mpmath
```

### Generate Figures
```bash
python3 code/chern_stratification.py
python3 code/dissipative_laplacian.py
python3 code/filippov_ricci_flow.py
python3 code/holonomy_interference.py
```

---

## Key Concepts

### Dissipative Categories
Small categories equipped with an additive entropy-production functional Σ that enforces causal rigidity: W(f) = 1 ⟺ f = id.

### Filippov–Ricci Flow
Evolution under nonsmooth curvature:
Ẇₜ(f) ∈ −Ric_JS^Fil(f, Wₜ) · Wₜ(f)
Curvature is not smoothed — it is *amplified*.

### Dissipative Laplacian
Not a classical Laplacian. Records instantaneous deformation of diffusion:
Δₜ = −Ṗₜ
where Pₜ is a geometric probe, not a Markov propagator.

### Complex Holonomy
Hol(γ) = exp(−Σ(γ)) · exp(−i·Φ(γ))
Magnitude = dissipation. Phase = curvature. Interference = geometry.

### Ternary Chern Classification
For L(s) ≠ 0:
c₁(L(s)) ∈ {−1, 0, +1}
Phase-first: records winding of normalized phase Θₗ(s) = L(s)/|L(s)| ∈ S¹.

---

## Citation

```bibtex
@article{souza2025dissipative,
  title={Dissipative Systems: From the Second Law of Thermodynamics to Filippov--Ricci Geometry},
  author={Souza Junior, Reinaldo Elias de},
  year={2026},
  month={May},
  institution={Faculdade de Medicina, Universidade Federal de Goiás},
  doi={10.5281/zenodo.20339888}
}
```

---

## License

This work is released under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

---

## Contact

**Reinaldo Elias de Souza Junior**  
resj3336@gmail.com

---

**Note:** This framework introduces a new ontology for dissipative geometry. Classical differential-geometric intuitions (smooth connections, Chern–Weil theory, Markov semigroups) do not directly apply. The code validates the operational consistency of the definitions; the theory stands on its own axioms.