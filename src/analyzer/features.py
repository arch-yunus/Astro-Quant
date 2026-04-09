import pandas as pd
import numpy as np
from typing import List, Optional

class AstroFeatureEngineer:
    """
    High-density feature engineering for Astro-ML.
    Transforms raw coordinates into cyclical features and intensifiers.
    """

    def __init__(self):
        pass

    def generate_cyclical_features(self, df: pd.DataFrame, planets: List[str]) -> pd.DataFrame:
        """
        Applies sine and cosine transformations to planetary longitudes [0, 360].
        This preserves the circular nature of the celestial sphere.
        """
        fe_df = df.copy()
        for planet in planets:
            lon_col = f"{planet}_longitude"
            if lon_col in fe_df.columns:
                # Convert degrees to radians
                radians = np.deg2rad(fe_df[lon_col])
                fe_df[f"{planet}_sin"] = np.sin(radians)
                fe_df[f"{planet}_cos"] = np.cos(radians)
                
        return fe_df

    def create_lagged_features(self, df: pd.DataFrame, columns: List[str], lags: int = 3) -> pd.DataFrame:
        """
        Creates temporal shifts for predictive modeling.
        """
        fe_df = df.copy()
        for col in columns:
            for i in range(1, lags + 1):
                fe_df[f"{col}_lag_{i}"] = fe_df[col].shift(i)
        return fe_df

    def generate_ml_ready_set(self, df: pd.DataFrame, planets: List[str]) -> pd.DataFrame:
        """
        Full pipeline to prepare high-density features for Scikit-Learn.
        """
        # 1. Cyclical transforms
        df = self.generate_cyclical_features(df, planets)
        
        # 2. Daily price deltas / volatility
        df["price_change"] = df["close"].pct_change()
        df["volatility_20"] = df["price_change"].rolling(20).std()
        
        # 3. Label: Direction for the next day (0=Down, 1=Up)
        df["target_direction"] = (df["price_change"].shift(-1) > 0).astype(int)
        
        return df.dropna()
