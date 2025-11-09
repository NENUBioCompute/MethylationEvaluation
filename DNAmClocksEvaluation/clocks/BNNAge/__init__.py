from core.r_clock_base import RClockBase


class BNNAge(RClockBase):
    """BNN Age clock - matching BNNAge function"""

    def __init__(self, method_name: str = "BNNAge"):
        super().__init__(method_name)
    