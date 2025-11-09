from core.r_clock_base import RClockBase


class PedBE(RClockBase):
    """PedBE clock - matching PedBE function"""

    def __init__(self, method_name: str = "PedBE"):
        super().__init__(method_name)
    