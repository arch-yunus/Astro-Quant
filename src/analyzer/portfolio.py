import numpy as np
import pandas as pd
from typing import List, Dict, Any

class AstroPortfolioOptimizer:
    """
    High-density portfolio optimization for celestial-biased assets.
    Merges Modern Portfolio Theory (MPT) with Astro-Sentiment scores.
    """

    def __init__(self, assets: List[str]):
        self.assets = assets

    def calculate_optimal_weights(self, returns_df: pd.DataFrame) -> Dict[str, float]:
        """
        Calculates weights based on 'Equal Risk Contribution' (simplification of MPT).
        """
        # Calculate standard deviation as a proxy for risk
        vols = returns_df[self.assets].std()
        inv_vols = 1.0 / vols
        weights = inv_vols / inv_vols.sum()
        
        return weights.to_dict()

    def adjust_weights_by_astro(self, weights: Dict[str, float], 
                                sentiments: Dict[str, float]) -> Dict[str, float]:
        """
        Adjusts portfolio weights based on celestial sentiment [-1, +1].
        High sentiment increases weight, negative sentiment reduces it.
        """
        adjusted_weights = {}
        total = 0
        
        for asset, weight in weights.items():
            sentiment = sentiments.get(asset, 0)
            # Factor: (1 + sentiment * 0.5) -> range of [0.5x, 1.5x] weight adjustment
            adjusted_weights[asset] = weight * (1 + sentiment * 0.5)
            total += adjusted_weights[asset]
            
        # Re-normalize to ensure sum is 1.0
        for asset in adjusted_weights:
            adjusted_weights[asset] /= total
            
        return adjusted_weights
