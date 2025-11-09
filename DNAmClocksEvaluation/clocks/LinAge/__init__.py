from core.r_clock_base import RClockBase


class LinAge(RClockBase):
    """Lin Age clock - matching LinAge function"""

    def __init__(self, method_name: str = "LinAge"):
        super().__init__(method_name)
    