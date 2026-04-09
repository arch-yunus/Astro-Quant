import datetime
import swisseph as swe
import pandas as pd
from typing import Dict, Union, List

class AstroEngine:
    """
    High-density celestial mechanics engine using Swiss Ephemeris.
    Provides planetary positioning, aspects, and retrograde detection.
    """

    # Swiss Ephemeris Planet Identifiers
    PLANETS = {
        "Sun": swe.SUN,
        "Moon": swe.MOON,
        "Mercury": swe.MERCURY,
        "Venus": swe.VENUS,
        "Mars": swe.MARS,
        "Jupiter": swe.JUPITER,
        "Saturn": swe.SATURN,
        "Uranus": swe.URANUS,
        "Neptune": swe.NEPTUNE,
        "Pluto": swe.PLUTO
    }

    def __init__(self, ephe_path: str = None):
        """
        Initialize the engine. 
        If ephe_path is provided, use high-precision ephemeris files.
        """
        if ephe_path:
            swe.set_ephe_path(ephe_path)
        
        # Default flags: Swiss Ephemeris calculation with speed data
        self.flags = swe.FLG_SWIEPH | swe.FLG_SPEED

    def get_julian_day(self, dt: datetime.datetime) -> float:
        """Converts UTC datetime to Julian Day."""
        return swe.julday(dt.year, dt.month, dt.day, dt.hour + dt.minute / 60.0)

    def get_planetary_data(self, dt: datetime.datetime, planet_name: str) -> Dict[str, Union[float, bool]]:
        """
        Returns longitude, latitude, and orbital speed of a specific planet.
        """
        if planet_name not in self.PLANETS:
            raise ValueError(f"Unknown planet: {planet_name}")
        
        jd = self.get_julian_day(dt)
        planet_id = self.PLANETS[planet_name]
        
        # swe.calc_ut returns (6-item tuple of floats: lon, lat, dist, speed_lon, speed_lat, speed_dist, status_flag)
        data, status = swe.calc_ut(jd, planet_id, self.flags)
        
        return {
            "longitude": data[0],
            "latitude": data[1],
            "speed_longitude": data[3], # Speed in ecliptic longitude (deg/day)
            "is_retrograde": data[3] < 0
        }

    def get_aspect(self, dt: datetime.datetime, planet1: str, planet2: str) -> float:
        """
        Calculates the angular distance (aspect) between two planets. 
        Result is in degrees [0, 180].
        """
        pos1 = self.get_planetary_data(dt, planet1)
        pos2 = self.get_planetary_data(dt, planet2)
        
        diff = abs(pos1["longitude"] - pos2["longitude"])
        if diff > 180:
            diff = 360 - diff
            
        return diff

    def check_event(self, dt: datetime.datetime, planet_name: str, event_type: str = "Retrograde") -> bool:
        """
        Generic event checker (e.g., checking if Mercury is Retrograde).
        """
        data = self.get_planetary_data(dt, planet_name)
        if event_type == "Retrograde":
            return data["is_retrograde"]
        return False
