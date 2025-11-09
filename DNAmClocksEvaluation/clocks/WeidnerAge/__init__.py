from core.r_clock_base import RClockBase


class WeidnerAge(RClockBase):
    """Weidner Age clock - matching WeidnerAge function"""

    def __init__(self, method_name: str = "WeidnerAge"):
        super().__init__(method_name)
    