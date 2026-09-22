import ast
from typing import List

class ToolSecurityScanner:
    FORBIDDEN_NODES = {
        'os.system', 'os.popen', 'subprocess.Popen', 'subprocess.call', 
        'shutil.rmtree', 'os.remove', 'os.rmdir', 'builtins.eval', 'builtins.exec'
    }

    @staticmethod
    def is_safe(code: str) -> bool:
        try:
            tree = ast.parse(code)
            for node in ast.walk(tree):
                if isinstance(node, ast.Call):
                    func = node.func
                    if isinstance(func, ast.Name):
                        if func.id in ToolSecurityScanner.FORBIDDEN_NODES:
                            return False
                    elif isinstance(func, ast.Attribute):
                        full_name = f"{getattr(func.value, 'id', '')}.{func.attr}"
                        if full_name in ToolSecurityScanner.FORBIDDEN_NODES:
                            return False
            return True
        except SyntaxError:
            return False
