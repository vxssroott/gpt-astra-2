import pytest
from memory.graph.semantic_graph import KnowledgeGraph

def test_graph_relation():
    kg = KnowledgeGraph(storage_path="tests/temp_graph.json")
    kg.add_relation("A", "links", "B")
    assert "B" in kg.find_shortest_path("A", "B")
