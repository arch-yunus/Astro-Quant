# Astro-Quant: Academic & Mathematical Methodology

This document details the rigorous scientific and mathematical foundations of the Astro-Quant framework, following the **Academic Operating System (AOS)** and **Medresetü’z-Zehra** vision.

## 01. Celestial Coordinate Systems
Astro-Quant utilizes the **Geocentric Ecliptic Coordinate System** as the primary frame of reference. Planetary positions are calculated using the **Swiss Ephemeris (DE431/DE441)**, providing millisecond-precision ephemeris data from -13,000 BCE to 16,800 CE.

## 02. Feature Normalization & Cyclical Transforms
Raw ecliptic longitude ($\lambda \in [0, 360)$) is intrinsically periodic. To avoid discontinuities at $0^\circ \equiv 360^\circ$ for machine learning models, we apply cyclical transformations:
$$ \sin(\lambda_{rad}) = \sin\left(\frac{2\pi \cdot \lambda}{360}\right) $$
$$ \cos(\lambda_{rad}) = \cos\left(\frac{2\pi \cdot \lambda}{360}\right) $$
This ensures that the distance between $359^\circ$ and $1^\circ$ is correctly mapped in the feature space.

## 03. Statistical Significance & Null Hypothesis Testing
To prevent spurious correlations (e.g., "The Texas Sharpshooter Fallacy"), Astro-Quant employs p-value testing to verify the significance of planetary impacts.
- **Null Hypothesis ($H_0$)**: Celestial events (e.g., Mercury Retrograde) have no impact on market volatility beyond random variance.
- **Verification**: GARCH (Generalized Autoregressive Conditional Heteroskedasticity) modeling is used to filter baseline volatility.

## 04. Macro-Cycle Confluence
Confluence is calculated as the weighted sum of normalized planetary speeds:
$$ Confluence = \sum_{p \in Planets} w_p \cdot \frac{v_p}{\max(v_p)} $$
where $v_p$ is the apparent orbital speed. A negative value indicates a cluster of retrogrades, signaling potential macro-liquidity contractions.

---
*AOS Theoretical Framework*
arch-yunus, 2026
