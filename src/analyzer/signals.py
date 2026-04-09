import pandas as pd
from typing import List, Dict, Optional

class ConfluenceEngine:
    """
    High-density confluence logic for celestial signals.
    Combines Multiple planetary retrogrades and aspects into a single 
    sentiment score [-1, +1].
    """

    def __init__(self, weights: Optional[Dict[str, float]] = None, use_ta: bool = True):
        """
        Weights for each planet in the sentiment calculation.
        use_ta: Whether to include traditional TA indicators.
        """
        self.use_ta = use_ta
        self.weights = weights or {
            "Mercury": 0.4,
            "Venus": 0.3,
            "Mars": 0.2,
            "Jupiter": 0.05,
            "Saturn": 0.05
        }

    def calculate_sentiment_score(self, df: pd.DataFrame) -> pd.Series:
        """
        Calculates a daily sentiment score based on weights.
        Direct (+) / Retrograde (-)
        """
        score = pd.Series(0.0, index=df.index)
        
        for planet, weight in self.weights.items():
            retro_col = f"{planet}_retrograde"
            if retro_col in df.columns:
                # Direct = +1, Retrograde = -1
                planet_influence = df[retro_col].apply(lambda x: -1.0 if x else 1.0)
                score += planet_influence * weight
        
        # Add TA Sentiment (RSI based)
        if self.use_ta and "rsi" in df.columns:
            # RSI < 30 (Oversold) -> Positive (+0.2 weight shift)
            # RSI > 70 (Overbought) -> Negative (-0.2 weight shift)
            ta_influence = df["rsi"].apply(lambda x: 0.2 if x < 30 else (-0.2 if x > 70 else 0.0))
            score += ta_influence
                
        return score

    def get_signal_zones(self, df: pd.DataFrame, threshold: float = 0.5) -> pd.Series:
        """
        Returns boolean series for Strong Buy (sentiment > threshold) 
        and Strong Sell (sentiment < -threshold).
        """
        sentiment = self.calculate_sentiment_score(df)
        signals = pd.Series(0, index=df.index)
        
        signals[sentiment > threshold] = 1   # Long
        signals[sentiment < -threshold] = -1 # Short
        
        return signals
