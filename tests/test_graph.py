from app.services.graph_store import GraphStore
from app.models.nodes import Node, Edge

def test_add_and_search():
    g = GraphStore()
    g.add_node(Node(id="a", label="Alpha"))
    g.add_node(Node(id="b", label="Beta"))
    g.add_edge(Edge(source="a", target="b", weight=1.2))
    res = g.search_label("alp")
    assert res and res[0][0] == "a"
    assert "b" in g.neighbors("a")
