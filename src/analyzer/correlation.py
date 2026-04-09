import pandas as pd
import numpy as np
from src.astro_engine.engine import AstroEngine
from typing import List, Dict, Optional

class AstroAnalyzer:
    """
    High-density quantitative analyzer for celestial-financial correlations.
    """

    def __init__(self, astro_engine: Optional[AstroEngine] = None):
        """Initialize with an optional AstroEngine instance."""
        self.engine = astro_engine or AstroEngine()

    def enrich_with_astro(self, df: pd.DataFrame, planets: List[str]) -> pd.DataFrame:
        """
        Enriches the financial DataFrame with planetary retrograde and position data.
        """
        enriched_df = df.copy()
        
        for planet in planets:
            # Generate retrograde and speed status for each timestamp
            planetary_data = enriched_df["timestamp"].apply(
                lambda x: self.engine.get_planetary_data(x, planet)
            )
            
            # Unpack the planetary data into columns
            enriched_df[f"{planet}_retrograde"] = planetary_data.apply(lambda x: x["is_retrograde"])
            enriched_df[f"{planet}_speed"] = planetary_data.apply(lambda x: x["speed_longitude"])
            enriched_df[f"{planet}_longitude"] = planetary_data.apply(lambda x: x["longitude"])
            
        return enriched_df

    def evaluate_performance(self, enriched_df: pd.DataFrame, planet: str) -> Dict[str, float]:
        """
        Calculates the performance metrics (Avg Return, Volatility) during retrograde vs direct.
        """
        # Calculate daily returns if not present
        if "return" not in enriched_df.columns:
            enriched_df["return"] = enriched_df["close"].pct_change()
            
        retro_mask = enriched_df[f"{planet}_retrograde"] == True
        direct_mask = enriched_df[f"{planet}_retrograde"] == False
        
        retro_returns = enriched_df.loc[retro_mask, "return"].dropna()
        direct_returns = enriched_df.loc[direct_mask, "return"].dropna()
        
        return {
            "retro_avg_return": float(retro_returns.mean()),
            "retro_volatility": float(retro_returns.std()),
            "direct_avg_return": float(direct_returns.mean()),
            "direct_volatility": float(direct_returns.std()),
            "n_retro_days": len(retro_returns),
            "n_direct_days": len(direct_returns)
        }

    def generate_report_summary(self, enriched_df: pd.DataFrame, planet: str) -> str:
        """
        Generates a text summary of the correlation findings.
        """
        stats = self.evaluate_performance(enriched_df, planet)
        
        summary = (
            f"--- {planet} Performance Analysis ---\n"
            f"Retrograde Days: {stats['n_retro_days']} Days\n"
            f"Direct Days: {stats['n_direct_days']} Days\n"
            f"Avg Return (Retro): {stats['retro_avg_return']:.4%}\n"
            f"Avg Return (Direct): {stats['direct_avg_return']:.4%}\n"
            f"Volatility (Retro): {stats['retro_volatility']:.4%}\n"
            f"Volatility (Direct): {stats['direct_volatility']:.4%}\n"
        )
        return summary
