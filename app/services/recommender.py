from typing import List, Tuple
from app.services.graph_store import GraphStore

class Recommender:
    def __init__(self, graph_store: GraphStore):
        self.graph = graph_store

    def suggest_next(self, node_id: str, k: int = 5) -> List[Tuple[str, float]]:
        neighbors = self.graph.neighbors(node_id)
        scored = []
        for n in neighbors:
            edge_data = self.graph.G.get_edge_data(node_id, n) or {}
            scored.append((n, float(edge_data.get("weight", 1.0))))
        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[:k]
