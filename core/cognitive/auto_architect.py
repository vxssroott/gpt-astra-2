import os
from typing import Tuple

class AutoArchitect:
    def __init__(self, core_dir: str = "core"):
        self.core_dir = core_dir

    def read_core_file(self, file_path: str) -> str:
        full_path = os.path.join(self.core_dir, file_path)
        with open(full_path, "r") as f:
            return f.read()

    def apply_patch(self, file_path: str, new_code: str):
        full_path = os.path.join(self.core_dir, file_path)
        with open(full_path, "w") as f:
            f.write(new_code)

    def propose_refactor(self, file_path: str, bridge: Any) -> str:
        current_code = self.read_core_file(file_path)
        prompt = f"Refactor this code for production grade. Return ONLY code:\n\n{current_code}"
        return bridge.call(prompt, system_prompt="You are ASTRA's Chief Architect.")
