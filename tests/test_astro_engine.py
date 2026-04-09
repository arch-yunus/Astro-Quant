import unittest
import datetime
from src.astro_engine.engine import AstroEngine

class TestAstroEngine(unittest.TestCase):
    """
    Unit tests for High-Density AstroEngine.
    """

    def setUp(self):
        self.engine = AstroEngine()

    def test_julian_day_calculation(self):
        # Known Julian Day for 2000-01-01 12:00:00 UTC is 2451545.0
        dt = datetime.datetime(2000, 1, 1, 12, 0)
        jd = self.engine.get_julian_day(dt)
        self.assertEqual(jd, 2451545.0)

    def test_planetary_position_range(self):
        # Longitude should always be between 0 and 360
        dt = datetime.datetime.now()
        data = self.engine.get_planetary_data(dt, "Mercury")
        self.assertGreaterEqual(data["longitude"], 0)
        self.assertLess(data["longitude"], 360)

    def test_lunar_phase_range(self):
        dt = datetime.datetime.now()
        phase = self.engine.get_lunar_phase(dt)
        self.assertGreaterEqual(phase, 0)
        self.assertLess(phase, 360)

if __name__ == "__main__":
    unittest.main()
