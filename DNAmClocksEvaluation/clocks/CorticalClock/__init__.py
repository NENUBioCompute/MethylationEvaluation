from core.r_clock_base import RClockBase


class CorticalClock(RClockBase):
    """Cortical Clock - matching CorticalClock function"""

    def __init__(self, method_name: str = "CorticalClock"):
        super().__init__(method_name)
    