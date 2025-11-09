from core.python_clock_base import PythonClockBase

class PerSEClock(PythonClockBase):
    """PerSEClock"""
    
    def __init__(self, method_name: str = "PerSEClock"):
        super().__init__(method_name)