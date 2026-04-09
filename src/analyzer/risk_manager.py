import pandas as pd
import numpy as np
from typing import Dict, List, Optional

class RiskManager:
    """
    High-density risk management engine for Astro-Quant.
    Calculates position sizes, stop-losses, and portfolio risk.
    """

    def __init__(self, risk_per_trade: float = 0.02, initial_capital: float = 10000.0):
        """
        risk_per_trade: Percentage of capital at risk per trade (default 2%).
        """
        self.risk_per_trade = risk_per_trade
        self.capital = initial_capital

    def calculate_atr(self, df: pd.DataFrame, window: int = 14) -> pd.Series:
        """
        Calculates Average True Range (ATR) as a measure of high-density volatility.
        """
        high_low = df["high"] - df["low"]
        high_close = (df["high"] - df["close"].shift(1)).abs()
        low_close = (df["low"] - df["close"].shift(1)).abs()
        
        tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
        atr = tr.rolling(window=window).mean()
        return atr

    def calculate_position_size(self, current_price: float, stop_loss_price: float) -> float:
        """
        Calculates the amount to buy based on the distance to the stop-loss.
        """
        risk_amount = self.capital * self.risk_per_trade
        distance_to_stop = abs(current_price - stop_loss_price)
        
        if distance_to_stop == 0:
            return 0
            
        position_qty = risk_amount / distance_to_stop
        return position_qty

    def get_volatility_stop_loss(self, current_price: float, atr: float, multiplier: float = 2.0) -> float:
        """
        Returns a stop-loss price level based on n-times ATR volatility.
        """
        return current_price - (atr * multiplier)
