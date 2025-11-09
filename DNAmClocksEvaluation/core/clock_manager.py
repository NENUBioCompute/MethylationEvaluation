import importlib
from pathlib import Path
from typing import Dict, Type, List
import pandas as pd
from .base_clock import BaseClock

class ClockManager:
    """
    Manages different methylation clock methods.
    Automatically discovers and loads available clock methods from the 'clocks' directory.
    """
    
    def __init__(self):
        self.available_methods: Dict[str, Type[BaseClock]] = {}
        self._discover_methods()
    
    def _discover_methods(self) -> None:
        """Automatically discover all available clock methods.
        Looks for subdirectories in the 'clocks' directory that contain an __init__.py file.
        """
        methods_path = Path(__file__).parent.parent / "clocks"
        
        for method_dir in methods_path.iterdir():
            if method_dir.is_dir() and (method_dir / "__init__.py").exists():
                method_name = method_dir.name
                try:
                    # Dynamically import the method module
                    module_path = f"clocks.{method_name}"
                    module = importlib.import_module(module_path)

                    # Assume the class name matches the method name
                    class_name = method_name
                    clock_class = getattr(module, class_name, None)
                    if clock_class and issubclass(clock_class, BaseClock):
                        self.available_methods[method_name] = clock_class
                        
                except Exception as e:
                    print(f"Warning: Failed to load method {method_name}: {e}")
    
    def list_methods(self) -> List[str]:
        """
        List all available clock methods.
        Returns:
            List[str]: List of method names.
        """
        return list(self.available_methods.keys())
    
    def get_clock(self, method_name: str) -> BaseClock:
        """Get the clock instance for the specified method. 
        Args:
            method_name (str): Name of the clock method.
        Returns:
            BaseClock: Instance of the clock method.
        Raises:
            ValueError: If the method is not found.
        """
        if method_name not in self.available_methods:
            raise ValueError(f"Method '{method_name}' not found. Available methods: {self.list_methods()}")
        
        clock_class = self.available_methods[method_name]
        return clock_class(method_name)
    
    def predict(self, method_name: str, input_file: str, **kwargs) -> pd.DataFrame:
        """Perform age prediction using the specified clock method.
        Args:
            method_name (str): Name of the clock method.
            input_file (str): Path to the input methylation data file.
            **kwargs: Additional arguments for the predict method.
        Returns:
            pd.DataFrame: DataFrame containing prediction results.
        """
        clock = self.get_clock(method_name)
        return clock.predict(input_file, **kwargs)

# Global manager instance
clock_manager = ClockManager()