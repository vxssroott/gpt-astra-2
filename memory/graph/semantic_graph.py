from typing import List, Tuple, Dict, Set

class KnowledgeGraph:
    """
    Moves memory from linear text to an Entity-Relationship Graph.
    Stores knowledge as (Subject)-[Predicate]->(Object).
    """
    def __init__(self):
        self.graph: Dict[str, Set[Tuple[str, str]]] = {}

    def add_relation(self, subject: str, predicate: str, obj: str):
        if subject not in self.graph:
            self.graph[subject] = set()
        self.graph[subject].add((predicate, obj))
        print(f"[MEMORY] Recorded: ({subject})--[{predicate}]-->({obj})")

    def query(self, subject: str) -> List[Tuple[str, str]]:
        return list(self.graph.get(subject, []))

    def find_path(self, start: str, end: str, max_depth: int = 3) -> List[str]:
        # Simple BFS to find relational paths between entities
        queue = [(start, [start])]
        visited = {start}
        
        while queue:
            (node, path) = queue.pop(0)
            if node == end:
                return path
            
            if len(path) <= max_depth:
                for pred, obj in self.graph.get(node, []):
                    if obj not in visited:
                        visited.add(obj)
                        queue.append((obj, path + [obj]))
        return []

# Test Graph
if __name__ == "__main__":
    kg = KnowledgeGraph()
    kg.add_relation("ASTRA", "creates", "ToolForge")
    kg.add_relation("ToolForge", "generates", "PythonCode")
    print(f"Path ASTRA -> PythonCode: {kg.find_path('ASTRA', 'PythonCode')}")
