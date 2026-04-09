import pandas as pd
import numpy as np
from typing import Dict, List, Optional

class AstroBacktester:
    """
    High-density algorithmic backtesting engine for celestial signals.
    Simulates portfolio growth, drawdown, and risk-adjusted returns.
    """

    def __init__(self, initial_capital: float = 10000.0, commission: float = 0.001):
        """
        initial_capital: Starting balance in USD/USDT.
        commission: Transaction fee per trade (default 0.1%).
        """
        self.initial_capital = initial_capital
        self.commission = commission

    def run_backtest(self, df: pd.DataFrame, signal_col: str) -> pd.DataFrame:
        """
        df: Enriched DataFrame with price and signal columns.
        signal_col: Boolean column (True = Long, False = Out).
        """
        results = df.copy()
        
        # Calculate strategy logic: Buy on signal (Market-on-Close)
        # We assume entry at the close of the signal day and exit at the close of the next non-signal day.
        results["position"] = results[signal_col].astype(int)
        results["trades"] = results["position"].diff().fillna(0).abs()
        
        # Returns calculation
        results["market_return"] = results["close"].pct_change()
        results["strategy_return"] = results["position"].shift(1) * results["market_return"]
        
        # Deduct commissions on trade execution
        results["costs"] = results["trades"] * self.commission
        results["net_strategy_return"] = results["strategy_return"] - results["costs"]
        
        # Cumulative growth
        results["cum_market_return"] = (1 + results["market_return"]).cumprod()
        results["cum_strategy_return"] = (1 + results["net_strategy_return"]).cumprod()
        
        # Equity curve
        results["equity"] = self.initial_capital * results["cum_strategy_return"]
        
        return results

    def calculate_performance_metrics(self, results: pd.DataFrame) -> Dict[str, float]:
        """
        Computes Sharpe Ratio, Max Drawdown, and Total Return.
        """
        total_return = (results["equity"].iloc[-1] / self.initial_capital) - 1
        
        # Sharpe Ratio (annualized, assuming daily data)
        daily_returns = results["net_strategy_return"].dropna()
        sharpe = np.sqrt(252) * daily_returns.mean() / daily_returns.std() if daily_returns.std() != 0 else 0
        
        # Max Drawdown
        rolling_max = results["equity"].cummax()
        drawdown = (results["equity"] - rolling_max) / rolling_max
        max_drawdown = drawdown.min()
        
        return {
            "total_return": total_return,
            "annualized_sharpe": sharpe,
            "max_drawdown": max_drawdown,
            "final_equity": results["equity"].iloc[-1]
        }
