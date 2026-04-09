import ccxt
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from typing import Optional, List

class DataFetcher:
    """
    High-density financial data ingestion service.
    Supports Crypto (via CCXT) and Stocks/Commodities (via YFinance).
    """

    def __init__(self, exchange_id: str = "binance"):
        """Initialize with a default exchange for CCXT."""
        self.exchange_id = exchange_id
        self.exchange = getattr(ccxt, exchange_id)({"enableRateLimit": True})

    def fetch_crypto(self, symbol: str = "BTC/USDT", timeframe: str = "1d", 
                      start_date: Optional[datetime] = None, limit: int = 1000) -> pd.DataFrame:
        """
        Fetches historical crypto OHLCV data from CCXT.
        """
        since = None
        if start_date:
            since = int(start_date.timestamp() * 1000)
        
        # ccxt.fetch_ohlcv returns list of lists: [timestamp, open, high, low, close, volume]
        ohlcv = self.exchange.fetch_ohlcv(symbol, timeframe, since, limit)
        
        df = pd.DataFrame(ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"])
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms", utc=True)
        return df

    def fetch_stock(self, symbol: str = "GC=F", period: str = "10y") -> pd.DataFrame:
        """
        Fetches historical stock/commodity data from YFinance.
        Example: Gold (Gold Futures) is 'GC=F'.
        """
        ticker = yf.Ticker(symbol)
        df = ticker.history(period=period)
        
        # Reset index to have 'Date' as a column and rename standard columns
        df.reset_index(inplace=True)
        df.rename(columns={"Date": "timestamp", "Open": "open", "High": "high", "Low": "low", "Close": "close", "Volume": "volume"}, inplace=True)
        df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
        return df

    def normalize_market_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Ensures standard column set and sorts by timestamp."""
        cols = ["timestamp", "open", "high", "low", "close", "volume"]
        df = df[cols].copy()
        df.sort_values("timestamp", inplace=True)
        df.reset_index(drop=True, inplace=True)
        return df
