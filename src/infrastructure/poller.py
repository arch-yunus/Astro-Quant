import time
import datetime
from typing import Callable, List, Optional

class RealTimePoller:
    """
    High-density real-time polling infrastructure.
    Monitors market data and triggers celestial analysis at specified intervals.
    """

    def __init__(self, interval_seconds: int = 60):
        self.interval = interval_seconds
        self.running = False

    def start_polling(self, assets: List[str], callback: Callable):
        """
        Starts a high-density polling loop.
        callback: Function to run on each iteration (e.g., a logic check).
        """
        print(f"--- [Astro-Quant Poller: Started ({self.interval}s interval)] ---")
        self.running = True
        
        try:
            while self.running:
                now = datetime.datetime.now()
                print(f"[{now.strftime('%H:%M:%S')}] Polling {len(assets)} assets...")
                
                # Execute logic
                callback(assets)
                
                # Wait for next interval
                time.sleep(self.interval)
        except KeyboardInterrupt:
            self.stop_polling()

    def stop_polling(self):
        print("--- [Astro-Quant Poller: Stopped] ---")
        self.running = False
