from core.r_clock_base import RClockBase


class PhenoAge(RClockBase):
    """PhenoAge clock - matching PhenoAge function"""

    def __init__(self, method_name: str = "PhenoAge"):
        super().__init__(method_name)
    