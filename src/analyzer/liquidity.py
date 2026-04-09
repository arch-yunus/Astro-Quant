import pandas as pd
import numpy as np
from src.astro_engine.engine import AstroEngine
from typing import Dict, Any

class LiquidityAnalyzer:
    """
    High-density analyzer for celestial-liquidity correlations.
    Specializes in Lunar Phase vs. DeFi TVL analysis.
    """

    def __init__(self, engine: AstroEngine):
        self.engine = engine

    def correlate_lunar_liquidity(self, df: pd.DataFrame, liquidity_col: str = "liquidity") -> Dict[str, Any]:
        """
        Analyzes if specific Lunar phases correlate with liquidity injections or withdrawals.
        """
        if liquidity_col not in df.columns:
            return {"error": "Liquidity column not found"}
            
        # Add Lunar Phase if not present
        if "lunar_phase" not in df.columns:
            df["lunar_phase"] = df["timestamp"].apply(lambda x: self.engine.get_lunar_phase(x))
            
        # Group by phases: 0-90 (New), 90-180 (Waxing), 180-270 (Full), 270-360 (Waning)
        df["phase_name"] = pd.cut(df["lunar_phase"], 
                                  bins=[0, 90, 180, 270, 360], 
                                  labels=["New Moon", "Waxing", "Full Moon", "Waning"])
                                  
        stats = df.groupby("phase_name")[liquidity_col].agg(["mean", "std", "count"])
        
        # Calculate volatility during phases
        df["liq_delta"] = df[liquidity_col].pct_change()
        vol_stats = df.groupby("phase_name")["liq_delta"].apply(lambda x: x.std() * np.sqrt(365))
        
        return {
            "liquidity_stats": stats.to_dict(),
            "lunar_volatility": vol_stats.to_dict()
        }
