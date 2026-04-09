import unittest
import pandas as pd
import numpy as np
from src.analyzer.backtester import AstroBacktester
from src.analyzer.risk_manager import RiskManager

class TestAnalyzer(unittest.TestCase):
    """
    Unit tests for Quantitative Analyzer modules.
    """

    def setUp(self):
        # Create a dummy dataset for testing
        data = {
            "timestamp": pd.date_range(start="2023-01-01", periods=10, freq="D"),
            "open": [100, 110, 105, 115, 120, 118, 125, 130, 128, 135],
            "high": [115, 120, 115, 125, 130, 125, 135, 140, 135, 145],
            "low": [95, 105, 100, 110, 115, 110, 120, 125, 120, 130],
            "close": [110, 105, 115, 120, 118, 125, 130, 128, 135, 140],
            "volume": [1000] * 10,
            "signal": [True, False, True, True, False, True, True, False, True, True]
        }
        self.df = pd.DataFrame(data)
        self.backtester = AstroBacktester(initial_capital=1000, commission=0)
        self.risk_manager = RiskManager(initial_capital=1000)

    def test_backtest_return_logic(self):
        results = self.backtester.run_backtest(self.df, "signal")
        # Final equity should be greater than initial capital since close went from 110 to 140 with mostly True signals
        self.assertGreater(results["equity"].iloc[-1], 1000)

    def test_risk_manager_position_sizing(self):
        # If risk is 2% of 1000 ($20) and stop-loss distance is $10 per unit, qty should be 2.0
        qty = self.risk_manager.calculate_position_size(current_price=100, stop_loss_price=90)
        self.assertEqual(qty, 2.0)

    def test_backtest_commission_impact(self):
        bt_fees = AstroBacktester(initial_capital=1000, commission=0.1) # Extreme fees
        results = bt_fees.run_backtest(self.df, "signal")
        self.assertLess(results["equity"].iloc[-1], 1000)

if __name__ == "__main__":
    unittest.main()
