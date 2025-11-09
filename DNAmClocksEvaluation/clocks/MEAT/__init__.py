from core.r_clock_base import RClockBase


class MEAT(RClockBase):
    """MEAT clock - matching MEAT function"""

    def __init__(self, method_name: str = "MEAT"):
        super().__init__(method_name)
    