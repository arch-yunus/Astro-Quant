import logging
import datetime
import os

class CelestialJournal:
    """
    High-density unified journal for tracking celestial-macro events.
    Records planetary cycles and corresponding market reactions.
    """

    def __init__(self, log_file: str = "logs/celestial_journal.log"):
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        
        self.logger = logging.getLogger("CelestialJournal")
        self.logger.setLevel(logging.INFO)
        
        # Avoid duplicate handlers
        if not self.logger.handlers:
            handler = logging.FileHandler(log_file)
            formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    def log_event(self, celestial_state: str, market_action: str, action_taken: str = "NONE"):
        """
        Logs a unified event entry.
        celestial_state: e.g. "Mercury Retrograde Begins"
        market_action: e.g. "BTC-USD Volatility Spillover (+5%)"
        action_taken: e.g. "Mock BUY Order Placed"
        """
        log_msg = f"EVENT: {celestial_state} | MARKET: {market_action} | ACTION: {action_taken}"
        self.logger.info(log_msg)
        print(f"[Journal] {log_msg}")

    def get_todays_outlook(self, planetary_states: dict) -> str:
        """
        Generates a summary string for the current celestial state.
        """
        summary = " | ".join([f"{p}: {'Retro' if s['retrograde'] else 'Direct'}" 
                             for p, s in planetary_states.items()])
        return summary
