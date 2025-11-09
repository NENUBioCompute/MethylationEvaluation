from core.r_clock_base import RClockBase

class HorvathAge(RClockBase):
    """Horvath 2013 epigenetic clock """
    
    def __init__(self, method_name: str = "HorvathAge"):
        super().__init__(method_name)
    