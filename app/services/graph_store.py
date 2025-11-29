import networkx as nx
from typing import List, Tuple, Optional
from app.models.nodes import Node, Edge

class GraphStore:
    def __init__(self):
        self.G = nx.Graph()

    def add_node(self, node: Node):
        self.G.add_node(node.id, label=node.label, meta=node.meta)

    def add_edge(self, edge: Edge):
        # avoid self-loops unless intended
        if edge.source == edge.target:
            return
        self.G.add_edge(edge.source, edge.target, weight=edge.weight, kind=edge.kind)

    def neighbors(self, node_id: str) -> List[str]:
        if node_id not in self.G:
            return []
        return list(self.G.neighbors(node_id))

    def search_label(self, query: str, limit: int = 12) -> List[Tuple[str, str]]:
        q = query.lower()
        matches = [
            (n, d.get("label", ""))
            for n, d in self.G.nodes(data=True)
            if q in d.get("label", "").lower()
        ]
        return matches[:limit]

    def get_node(self, node_id: str) -> Optional[dict]:
        if node_id in self.G:
            data = self.G.nodes[node_id]
            return {"id": node_id, "label": data.get("label"), "meta": data.get("meta", {})}
        return None

    def ensure_node(self, node_id: str, label: Optional[str] = None):
        if node_id not in self.G:
            self.add_node(Node(id=node_id, label=label or node_id))
