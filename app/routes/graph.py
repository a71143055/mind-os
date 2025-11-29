from fastapi import APIRouter
from typing import List, Dict, Any
from app.models.nodes import Node, Edge
from app.services.graph_store import GraphStore

def get_router(graph: GraphStore) -> APIRouter:
    router = APIRouter(prefix="/graph", tags=["graph"])

    @router.post("/node")
    def add_node(node: Node):
        graph.add_node(node)
        return {"ok": True, "node": node.model_dump()}

    @router.post("/edge")
    def add_edge(edge: Edge):
        graph.add_edge(edge)
        return {"ok": True, "edge": edge.model_dump()}

    @router.get("/search")
    def search(q: str):
        results = graph.search_label(q)
        return {"results": [{"id": nid, "label": label} for nid, label in results]}

    @router.get("/node/{node_id}")
    def get_node(node_id: str) -> Dict[str, Any]:
        n = graph.get_node(node_id)
        return {"node": n}

    @router.get("/neighbors/{node_id}")
    def neighbors(node_id: str) -> List[str]:
        return graph.neighbors(node_id)

    return router
