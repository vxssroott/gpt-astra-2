import asyncio
from typing import List, Dict, Any
from dataclasses import dataclass

@dataclass
class AgentPersona:
    role: str
    specialization: str
    directives: str

class SwarmAgent:
    def __init__(self, agent_id: str, persona: AgentPersona, bridge: Any):
        self.agent_id = agent_id
        self.persona = persona
        self.bridge = bridge

    async def execute_task(self, task: str) -> str:
        system_prompt = f"You are {self.persona.role}, specializing in {self.persona.specialization}. {self.persona.directives}"
        return self.bridge.call(task, system_prompt=system_prompt)

class SwarmController:
    def __init__(self, bridge: Any):
        self.bridge = bridge
        self.agents: Dict[str, SwarmAgent] = {}
        self._setup_default_swarm()

    def _setup_default_swarm(self):
        personas = {
            "Researcher": AgentPersona("Researcher", "OSINT", "Prioritize primary sources."),
            "Architect": AgentPersona("Architect", "System Design", "Focus on scalability."),
            "Critic": AgentPersona("Critic", "Adversarial Analysis", "Identify flaws."),
            "Coder": AgentPersona("Coder", "Implementation", "Write production Python.")
        }
        for role, persona in personas.items():
            self.agents[role] = SwarmAgent(role, persona, self.bridge)

    async def dispatch(self, task_map: Dict[str, str]) -> Dict[str, Any]:
        tasks = []
        roles = []
        for role, task in task_map.items():
            if role in self.agents:
                tasks.append(self.agents[role].execute_task(task))
                roles.append(role)
        results = await asyncio.gather(*tasks)
        return dict(zip(roles, results))
