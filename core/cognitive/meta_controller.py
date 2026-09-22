import asyncio
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from core.tools.forge import ToolForge
from memory.graph.semantic_graph import KnowledgeGraph

@dataclass
class CognitiveState:
    goal: str
    hypothesis: str
    evidence: List[Any]
    confidence: float
    reflection: str
    critical_flaw: Optional[str] = None

class MetaController:
    """
    ASTRA 2.0 MetaController: Integrated with Self-Evolution (Forge) 
    and Semantic Memory (Graph).
    """
    def __init__(self):
        self.state = CognitiveState(goal="", hypothesis="", evidence=[], confidence=0.0, reflection="")
        self.forge = ToolForge()
        self.memory = KnowledgeGraph()

    async def perceive(self, input_data: str):
        print(f"\n[PERCEPTION] Input: {input_data}")
        self.state.goal = input_data
        return await self.hypothesize()

    async def hypothesize(self):
        print("[HYPOTHESIS] Strategy: Deploy probes and verify via Adversarial Critic.")
        self.state.hypothesis = "Verify goal using specialized tools and relational memory."
        return await self.execute()

    async def execute(self):
        print("[EXECUTION] Executing cognitive tasks...")
        
        # Example of using the Forge to create a tool on the fly
        if "calculate" in self.state.goal.lower():
            calc_tool = self.forge.forge_tool("fast_calc", "def run(x): return x * 1.1")
            self.state.evidence.append(calc_tool(100))
        
        # Store discovery in Semantic Memory
        self.memory.add_relation("ASTRA", "processed", self.state.goal)
        self.state.evidence.append("Relational link created in memory.")
        
        return await self.criticize()

    async def criticize(self):
        print("[ADVERSARIAL CRITIC] Attempting to debunk current evidence...")
        # The Critic simulates a second agent trying to find a flaw
        if len(self.state.evidence) < 2:
            self.state.critical_flaw = "Insufficient evidence to support hypothesis."
            self.state.confidence = 0.3
        else:
            self.state.critical_flaw = None
            self.state.confidence = 0.8
        
        return await self.reflect()

    async def reflect(self):
        print("[REFLECTION] Analyzing Critic findings...")
        if self.state.critical_flaw:
            print(f"Flaw found: {self.state.critical_flaw}. Restarting loop...")
            self.state.reflection = "Failure: Evidence too thin."
            return await self.hypothesize()
        
        print("Goal achieved. Confidence high.")
        return self.state

if __name__ == "__main__":
    astra = MetaController()
    # Test a a scenario that requires the "Forge"
    asyncio.run(astra.perceive("Please calculate the growth projection"))
