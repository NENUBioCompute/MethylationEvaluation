from core.python_clock_base import PythonClockBase

class EPM(PythonClockBase):
    """EPM(Epigenetic Pacemaker)"""
    
    def __init__(self, method_name: str = "EPM"):
        super().__init__(method_name)