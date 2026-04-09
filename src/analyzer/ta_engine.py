import pandas as pd
import numpy as np

class TechnicalAnalysisEngine:
    """
    High-density technical analysis engine for Astro-Quant.
    Calculates standard financial indicators to complement celestial signals.
    """

    def __init__(self):
        pass

    def calculate_rsi(self, series: pd.Series, period: int = 14) -> pd.Series:
        """
        Calculates Relative Strength Index (RSI).
        """
        delta = series.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs))

    def calculate_macd(self, series: pd.Series) -> pd.DataFrame:
        """
        Calculates Moving Average Convergence Divergence (MACD).
        """
        exp1 = series.ewm(span=12, adjust=False).mean()
        exp2 = series.ewm(span=26, adjust=False).mean()
        macd = exp1 - exp2
        signal = macd.ewm(span=9, adjust=False).mean()
        return pd.DataFrame({"macd": macd, "signal": signal, "hist": macd - signal})

    def calculate_bollinger_bands(self, series: pd.Series, window: int = 20) -> pd.DataFrame:
        """
        Calculates Bollinger Bands.
        """
        sma = series.rolling(window=window).mean()
        std = series.rolling(window=window).std()
        return pd.DataFrame({
            "upper": sma + (std * 2),
            "lower": sma - (std * 2),
            "mid": sma
        })

    def enrich_df(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Adds TA indicators to the main DataFrame.
        """
        res = df.copy()
        res["rsi"] = self.calculate_rsi(res["close"])
        
        macd_df = self.calculate_macd(res["close"])
        res["macd"] = macd_df["macd"]
        res["macd_signal"] = macd_df["signal"]
        
        bb_df = self.calculate_bollinger_bands(res["close"])
        res["bb_upper"] = bb_df["upper"]
        res["bb_lower"] = bb_df["lower"]
        
        return res
