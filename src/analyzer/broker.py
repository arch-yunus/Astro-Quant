import pandas as pd
import datetime
from typing import Dict, Any, List

class MockBroker:
    """
    High-density mock execution layer for forward testing.
    Simulates real-time order execution, portfolio tracking, and PnL calculation.
    """

    def __init__(self, initial_usd: float = 10000.0):
        self.balance_usd = initial_usd
        self.holdings = {} # {asset: qty}
        self.trades = []
        self.equity_history = []

    def place_order(self, asset: str, side: str, price: float, qty: float):
        """
        Executes a mock order.
        side: 'BUY' or 'SELL'
        """
        cost = price * qty
        timestamp = datetime.datetime.now()
        
        if side == "BUY":
            if self.balance_usd >= cost:
                self.balance_usd -= cost
                self.holdings[asset] = self.holdings.get(asset, 0) + qty
                self.trades.append({
                    "timestamp": timestamp, "asset": asset, "side": side, 
                    "price": price, "qty": qty, "total": cost
                })
                print(f"[Broker] MOCK BUY: {qty} {asset} at ${price:,.2f}")
            else:
                print(f"[Broker] Insufficient Balance for BUY {asset}")
                
        elif side == "SELL":
            current_qty = self.holdings.get(asset, 0)
            if current_qty >= qty:
                self.balance_usd += cost
                self.holdings[asset] -= qty
                self.trades.append({
                    "timestamp": timestamp, "asset": asset, "side": side, 
                    "price": price, "qty": qty, "total": cost
                })
                print(f"[Broker] MOCK SELL: {qty} {asset} at ${price:,.2f}")
            else:
                print(f"[Broker] Insufficient Holdings for SELL {asset}")

    def get_total_equity(self, current_prices: Dict[str, float]) -> float:
        """
        Calculates total portfolio value (USD + Holdings at current price).
        """
        equity = self.balance_usd
        for asset, qty in self.holdings.items():
            equity += qty * current_prices.get(asset, 0)
        return equity

    def export_trade_log(self) -> pd.DataFrame:
        """
        Returns a high-density trade log for academic review.
        """
        return pd.DataFrame(self.trades)
