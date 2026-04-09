from typing import Dict, Any

class ConfidenceAggregator:
    """
    High-density intelligence aggregator.
    Merges Astro, TA, and ML signals into a single Unified Confidence Index.
    """

    def __init__(self):
        self.weights = {
            "astro": 0.50,
            "ta": 0.25,
            "ml": 0.25
        }

    def aggregate_confidence(self, astro_score: float, rsi: float, ml_prob: float) -> float:
        """
        Calculates a Unified Confidence Score [0-100].
        astro_score: [-1, +1]
        rsi: [0, 100]
        ml_prob: [0, 1]
        """
        # Normalize inputs to [0, 1]
        n_astro = (astro_score + 1) / 2
        
        # TA Logic: RSI extremes = high confidence for trend reversal/continuance
        n_ta = 1.0 if (rsi < 30 or rsi > 70) else 0.5
        
        n_ml = ml_prob
        
        unified_score = (n_astro * self.weights["astro"] + 
                         n_ta * self.weights["ta"] + 
                         n_ml * self.weights["ml"]) * 100
                         
        return round(unified_score, 2)
