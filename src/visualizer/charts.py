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

    def plot_portfolio_performance(self, df: pd.DataFrame, 
                                   output_file: Optional[str] = None) -> go.Figure:
        """
        Visualizes the strategy performance: Equity Curve and Max Drawdown.
        """
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                           vertical_spacing=0.1, subplot_titles=("Strategy Equity Curve", "Daily Returns"),
                           row_width=[0.3, 0.7])

        # Equity Curve
        fig.add_trace(go.Scatter(x=df["timestamp"], y=df["equity"],
                                mode="lines", line=dict(color="green", width=2),
                                name="Portfolio Equity"), row=1, col=1)

        # Baseline: Initial Capital
        initial_cap = df["equity"].iloc[0]
        fig.add_hline(y=initial_cap, line_dash="dash", line_color="white", opacity=0.5, row=1, col=1)

        # Daily Returns
        fig.add_trace(go.Bar(x=df["timestamp"], y=df["net_strategy_return"] * 100, 
                            name="Daily ROI (%)", marker_color="royalblue", opacity=0.7), row=2, col=1)

        fig.update_layout(template=self.theme,
                         height=800,
                         title_text="Astro-Quant Algorithmic Performance Report",
                         showlegend=True)

        if output_file:
            fig.write_html(output_file)
            
        return fig
