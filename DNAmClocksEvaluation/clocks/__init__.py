from importlib import import_module

def run_clock(method_name, beta_path):
    try:
        module = import_module(f"clocks.{method_name}")
        clock = module.get_clock()
        return clock.run(beta_path)
    except ModuleNotFoundError:
        raise ValueError(f"Clock '{method_name}' not found.")
    except AttributeError:
        raise ValueError(f"Clock '{method_name}' does not have a 'get_clock' method.")
    