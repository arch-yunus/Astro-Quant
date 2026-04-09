import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from typing import List, Optional

class AstroVisualizer:
    """
    High-density visualization service for Astro-Quant reports.
    Uses Plotly for interactive data reports.
    """

    def __init__(self, theme: str = "plotly_dark"):
        """Initialize with a selected Plotly theme."""
        self.theme = theme

    def plot_candlesticks_with_events(self, df: pd.DataFrame, planet: str, 
                                     output_file: Optional[str] = None) -> go.Figure:
        """
        Generates a candlestick chart with celestial event overlays (e.g. Mercury Retrograde).
        """
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                           vertical_spacing=0.1, subplot_titles=(f"{planet} Retrograde vs Price Action", "Market Volume"), 
                           row_width=[0.2, 0.7])

        # Standard Candlestick
        fig.add_trace(go.Candlestick(x=df["timestamp"],
                                    open=df["open"], high=df["high"],
                                    low=df["low"], close=df["close"],
                                    name="Market Price"), row=1, col=1)

        # Highlight Retrograde Periods
        retro_mask = df[f"{planet}_retrograde"] == True
        retro_df = df[retro_mask]
        
        # Add markers for retrograde days
        fig.add_trace(go.Scatter(x=retro_df["timestamp"], y=retro_df["high"] * 1.02,
                                mode="markers", marker=dict(symbol="triangle-down", color="red", size=8),
                                name=f"{planet} Retrograde"), row=1, col=1)

        # Bottom Subplot: Market Volume
        fig.add_trace(go.Bar(x=df["timestamp"], y=df["volume"], name="Volume", marker_color="white", opacity=0.3), row=2, col=1)

        # Layout styling
        fig.update_layout(template=self.theme,
                         xaxis_rangeslider_visible=False,
                         height=800,
                         title_text=f"Astro-Quant Technical Report: {planet} Market Impact Analysis",
                         showlegend=True)

        if output_file:
            fig.write_html(output_file)
            
        return fig
