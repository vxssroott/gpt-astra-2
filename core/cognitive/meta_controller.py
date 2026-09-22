import asyncio
import logging
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from core.cognitive.modules.perceiver import Perceiver
from core.cognitive.modules.hypothesizer import Hypothesizer
from core.cognitive.modules.critic import Critic
from core.cognitive.modules.reflector import Reflector
from core.tools.forge import ToolForge
from memory.graph.semantic_graph import KnowledgeGraph

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("ASTRA-CORE")

@dataclass
class CognitiveState:
    goal: str
    hypothesis: str = ""
    evidence: List[Any] = field(default_factory=list)
    confidence: float = 0.0
    reflection: str = ""
    cycle_count: int = 0

class MetaController:
    def __init__(self):
        self.config = {"confidence_threshold": 0.85, "max_reflection_cycles": 3}
        self.state = CognitiveState(goal="")
        
        # Modules
        self.perceiver = Perceiver()
        self.hypothesizer = Hypothesizer()
        self.critic = Critic()
        self.reflector = Reflector()
        
        # Systems
        self.forge = ToolForge()
        self.memory = KnowledgeGraph()

    async def process(self, input_goal: str):
        logger.info(f"Entering Cognitive Loop: {input_goal}")
        self.state = CognitiveState(goal=input_goal)
        
        while self.state.confidence < self.config["confidence_threshold"]:
            if self.state.cycle_count >= self.config["max_reflection_cycles"]:
                break
            
            self.state.cycle_count += 1
            
            # 1. Perception
            perc = self.perceiver.analyze(self.state.goal)
            
            # 2. Hypothesis
            self.state.hypothesis = " ".join(self.hypothesizer.create_strategy(perc))
            
            # 3. Execution (Simulated tool trigger)
            if "calculate" in self.state.goal.lower():
                tool = self.forge.forge_tool("calc", "def run(): print('42')\nif __name__=='__main__': run()")
                self.state.evidence.append(self.forge.execute_tool("calc", []))
            
            # 4. Verification
            if self.critic.audit(self.state.evidence, self.state.goal):
                self.state.confidence = 0.9
            else:
                self.state.reflection = self.reflector.optimize("Insufficient evidence")
                self.state.confidence = 0.1
                
        return self.state

if __name__ == "__main__":
    astra = MetaController()
    asyncio.run(astra.process("Calculate orbital velocity"))
