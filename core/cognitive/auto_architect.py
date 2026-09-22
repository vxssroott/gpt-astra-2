import os
from typing import Tuple

class AutoArchitect:
    def __init__(self, core_dir: str = "core"):
        self.core_dir = core_dir

    def analyze_source(self, file_name: str) -> str:
        path = os.path.join(self.core_dir, file_name)
        with open(path, "r") as f:
            return f.read()

    def propose_refactor(self, file_name: str, current_code: str, improved_code: str) -> Tuple[str, str]:
        patch_name = f"refactor_{file_name}.patch"
        with open(patch_name, "w") as f:
            f.write(f"--- {file_name}\n+++ {file_name}_new\n\n{improved_code}")
        return patch_name, improved_code
