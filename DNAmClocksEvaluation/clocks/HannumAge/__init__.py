from core.r_clock_base import RClockBase


class HannumAge(RClockBase):
    """Hannum Age clock - matching HannumAge function"""

    def __init__(self, method_name: str = "HannumAge"):
        super().__init__(method_name)
    