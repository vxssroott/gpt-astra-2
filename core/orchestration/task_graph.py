from typing import Callable, List, Dict
import asyncio

class TaskNode:
    def __init__(self, name: str, action: Callable, dependencies: List[str] = None):
        self.name = name
        self.action = action
        self.dependencies = dependencies or []
        self.result = None
        self.completed = False

class TaskGraph:
    """
    Manages a Directed Acyclic Graph (DAG) of tasks for parallel execution.
    """
    def __init__(self):
        self.nodes: Dict[str, TaskNode] = {}

    def add_task(self, name: str, action: Callable, dependencies: List[str] = None):
        self.nodes[name] = TaskNode(name, action, dependencies)

    async def execute(self):
        pending = list(self.nodes.keys())
        while pending:
            executable = [
                name for name in pending 
                if all(self.nodes[dep].completed for dep in self.nodes[name].dependencies)
            ]
            
            if not executable:
                raise Exception("Deadlock detected in TaskGraph! Check dependencies.")

            # Run all available tasks in parallel
            tasks = [self._run_node(name) for name in executable]
            await asyncio.gather(*tasks)
            
            for name in executable:
                pending.remove(name)

    async def _run_node(self, name: str):
        node = self.nodes[name]
        print(f"[GRAPH] Executing: {node.name}")
        node.result = await node.action()
        node.completed = True

# Test the Graph
async def mock_action():
    await asyncio.sleep(0.1)
    return "Success"

async def test_graph():
    graph = TaskGraph()
    graph.add_task("A", mock_action)
    graph.add_task("B", mock_action)
    graph.add_task("C", mock_action, dependencies=["A", "B"])
    await graph.execute()
    print("Graph executed successfully.")

if __name__ == "__main__":
    asyncio.run(test_graph())
