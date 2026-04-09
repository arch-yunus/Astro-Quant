import plotly.graph_objects as go
import numpy as np
from typing import List, Dict, Any

class CelestialVisualizer:
    """
    High-density visualization engine for 3D celestial mapping.
    Visualizes planetary orbits and positions in 3D space.
    """

    def __init__(self):
        # Estimated orbital radii (AU) for visualization logic
        self.radii = {
            "Mercury": 0.39,
            "Venus": 0.72,
            "Mars": 1.52,
            "Jupiter": 5.20,
            "Saturn": 9.54,
            "Sun": 0.05
        }
        self.colors = {
            "Mercury": "gray", "Venus": "orange", "Mars": "red", 
            "Jupiter": "brown", "Saturn": "gold", "Sun": "yellow"
        }

    def plot_3d_solar_system(self, planetary_states: Dict[str, Any]) -> go.Figure:
        """
        Generates a 3D Plotly figure showing planetary orbits and current longitudes.
        """
        fig = go.Figure()

        # Add Sun
        fig.add_trace(go.Scatter3d(
            x=[0], y=[0], z=[0],
            mode="markers",
            marker=dict(size=12, color=self.colors["Sun"]),
            name="Sun (Center)"
        ))

        for planet, state in planetary_states.items():
            if planet not in self.radii: continue
            
            r = self.radii[planet]
            lon_rad = np.deg2rad(state["longitude"])
            
            # Current Position
            x = r * np.cos(lon_rad)
            y = r * np.sin(lon_rad)
            z = 0
            
            # Orbit Path
            theta = np.linspace(0, 2*np.pi, 100)
            ox = r * np.cos(theta)
            oy = r * np.sin(theta)
            oz = np.zeros(100)
            
            # Add Orbit trace
            fig.add_trace(go.Scatter3d(
                x=ox, y=oy, z=oz,
                mode="lines",
                line=dict(color=self.colors[planet], width=1, dash="dot"),
                hoverinfo="none", showlegend=False
            ))
            
            # Add Planet trace
            fig.add_trace(go.Scatter3d(
                x=[x], y=[y], z=[z],
                mode="markers+text",
                marker=dict(size=8, color=self.colors[planet]),
                text=[planet],
                textposition="top center",
                name=planet
            ))

        fig.update_layout(
            template="plotly_dark",
            scene=dict(
                xaxis_title="X (AU)", yaxis_title="Y (AU)", zaxis_title="Z (AU)",
                xaxis=dict(showgrid=False), yaxis=dict(showgrid=False), zaxis=dict(showgrid=False)
            ),
            title="3D Astro-Quant Celestial Mapping",
            margin=dict(l=0, r=0, b=0, t=40)
        )
        
        return fig
