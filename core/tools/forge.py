import os
import subprocess
import sys
from typing import Any
from core.tools.sandbox import ToolSecurityScanner

class ToolForge:
    def __init__(self, tools_dir: str = "core/tools/lib"):
        self.tools_dir = tools_dir
        os.makedirs(self.tools_dir, exist_ok=True)
        self.scanner = ToolSecurityScanner()

    def forge_tool(self, name: str, code: str) -> str:
        if not self.scanner.is_safe(code):
            raise PermissionError(f"Security Violation: Tool '{name}' contains forbidden system calls.")
            
        file_path = os.path.join(self.tools_dir, f"{name}.py")
        with open(file_path, "w") as f:
            f.write(code)
        return file_path

    def execute_tool(self, tool_name: str, args: list) -> Any:
        file_path = os.path.join(self.tools_dir, f"{tool_name}.py")
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Tool {tool_name} not forged.")
        
        try:
            result = subprocess.run(
                [sys.executable, file_path] + args,
                capture_output=True, text=True, timeout=30
            )
            return result.stdout.strip() if result.returncode == 0 else result.stderr
        except Exception as e:
            return f"Execution Error: {str(e)}"
