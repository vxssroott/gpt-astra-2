import os
import importlib.util
import sys
from typing import Callable, Any

class ToolForge:
    """
    The ToolForge allows ASTRA to write its own capabilities as Python files,
    test them, and then import them into the runtime dynamically.
    """
    def __init__(self, tools_dir: str = "core/tools"):
        self.tools_dir = tools_dir
        os.makedirs(self.tools_dir, exist_ok=True)

    def forge_tool(self, name: str, code: str) -> Callable:
        file_path = os.path.join(self.tools_dir, f"{name}.py")
        print(f"[FORGE] Materializing new capability: {name}...")
        
        with open(file_path, "w") as f:
            f.write(code)
        
        return self.load_tool(name)

    def load_tool(self, name: str) -> Callable:
        file_path = os.path.join(self.tools_dir, f"{name}.py")
        spec = importlib.util.spec_from_file_location(name, file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # Assume the main function is called 'run'
        if hasattr(module, 'run'):
            return module.run
        raise ImportError(f"Tool {name} must have a 'run()' function.")

# Test Forge
if __name__ == "__main__":
    forge = ToolForge()
    test_code = "def run(x): return f'Forged result: {x * 2}'"
    fn = forge.forge_tool("double_it", test_code)
    print(fn(10)) # Should be 20
