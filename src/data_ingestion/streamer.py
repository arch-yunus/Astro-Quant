import asyncio
import json
from typing import Callable, List

class AstroStreamer:
    """
    High-density real-time streaming ingestion.
    Provides WebSocket hooks for high-frequency market updates.
    """

    def __init__(self, exchange_id: str = "binance"):
        self.exchange_id = exchange_id

    async def connect_and_listen(self, symbols: List[str], on_tick: Callable):
        """
        Simulates connecting to a WebSocket (e.g., CCXT Pro) and listening 
        for ticker updates.
        """
        print(f"[Streamer] Connecting to {self.exchange_id} WebSocket...")
        
        # Simulate real-time ticks
        try:
            while True:
                for symbol in symbols:
                    # Mocking a tick update
                    tick = {"symbol": symbol, "price": 100.0, "timestamp": asyncio.get_event_loop().time()}
                    await on_tick(tick)
                    await asyncio.sleep(1) # Frequency control
        except asyncio.CancelledError:
            print("[Streamer] Connection Closed.")

    def run_stream(self, symbols: List[str], on_tick: Callable):
        """
        Entry point to start the event loop.
        """
        try:
            asyncio.run(self.connect_and_listen(symbols, on_tick))
        except KeyboardInterrupt:
            pass
