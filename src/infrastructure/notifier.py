import requests
import json
from typing import Dict, Any, Optional

class DiscordNotifier:
    """
    High-density notification service for Astro-Quant.
    Sends real-time signals and backtest reports to Discord via Webhooks.
    """

    def __init__(self, webhook_url: Optional[str] = None):
        """
        webhook_url: The Discord Webhook URL for the target channel.
        """
        self.webhook_url = webhook_url

    def send_log(self, message: str, title: str = "Astro-Quant Alert"):
        """
        Sends a simple text message to Discord.
        """
        if not self.webhook_url:
            print(f"[Notifier-Disabled] {title}: {message}")
            return
            
        payload = {
            "embeds": [{
                "title": title,
                "description": message,
                "color": 3447003 # Blue
            }]
        }
        
        try:
            requests.post(self.webhook_url, json=payload)
        except Exception as e:
            print(f"Error sending Discord notification: {e}")

    def send_trade_signal(self, asset: str, signal_type: str, sentiment: float):
        """
        Sends a formatted trade signal alert.
        """
        color = 3066993 if signal_type == "LONG" else 15158332 # Green/Red
        
        payload = {
            "embeds": [{
                "title": f"New Signal: {asset} ({signal_type})",
                "fields": [
                    {"name": "Asset", "value": asset, "inline": True},
                    {"name": "Signal", "value": signal_type, "inline": True},
                    {"name": "Celestial Sentiment", "value": f"{sentiment:.2f}", "inline": True}
                ],
                "color": color
            }]
        }
        
        if self.webhook_url:
            requests.post(self.webhook_url, json=payload)
        else:
            print(f"[Notifier-Disabled] {asset} Signal: {signal_type} ({sentiment:.2f})")
