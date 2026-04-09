import pandas as pd
import numpy as np
from src.analyzer.backtester import AstroBacktester
from src.analyzer.correlation import AstroAnalyzer
from typing import List, Dict, Any, Tuple

class AstroOptimizer:
    """
    High-density parameter optimizer for celestial signal tuning.
    Uses brute-force scanning to find the most profitable planetary orbs and aspects.
    """

    def __init__(self, df: pd.DataFrame, analyzer: AstroAnalyzer, backtester: AstroBacktester):
        self.df = df
        self.analyzer = analyzer
        self.backtester = backtester

    def optimize_retrograde_impact(self, planet: str, capital: float = 10000.0) -> Dict[str, Any]:
        """
        Scans both Long and Short scenarios for a specific planetary retrograde.
        Returns the best direction and its performance metrics.
        """
        results = []
        
        # Scenario 1: Long during Direct, Out during Retrograde (Default)
        df_enriched = self.analyzer.enrich_with_astro(self.df, planets=[planet])
        
        # Test Direct-Only (Long when Retrograde == False)
        df_enriched["signal_long"] = df_enriched[f"{planet}_retrograde"] == False
        perf_long = self.backtester.run_backtest(df_enriched, "signal_long")
        metrics_long = self.backtester.calculate_performance_metrics(perf_long)
        results.append({"mode": "Long-during-Direct", "metrics": metrics_long})
        
        # Test Retro-Only (Long when Retrograde == True)
        df_enriched["signal_retro"] = df_enriched[f"{planet}_retrograde"] == True
        perf_retro = self.backtester.run_backtest(df_enriched, "signal_retro")
        metrics_retro = self.backtester.calculate_performance_metrics(perf_retro)
        results.append({"mode": "Long-during-Retrograde", "metrics": metrics_retro})
        
        # Find best mode by Total Return
        best_mode = max(results, key=lambda x: x["metrics"]["total_return"])
        return {
            "best_mode": best_mode["mode"],
            "metrics": best_mode["metrics"]
        }

    def scan_multi_planet_confluence(self, planets: List[str]) -> pd.DataFrame:
        """
        Scans for confluence points where multiple planets share the same state.
        Useful for building 'High-Probability' signal zones.
        """
        df_enriched = self.analyzer.enrich_with_astro(self.df, planets=planets)
        
        # Confluence Score: Number of planets in 'Direct' motion (positive sentiment)
        df_enriched["confluence_score"] = 0
        for planet in planets:
            # We assume Direct (False) is +1, Retrograde (True) is 0
            df_enriched["confluence_score"] += (df_enriched[f"{planet}_retrograde"] == False).astype(int)
            
        return df_enriched
