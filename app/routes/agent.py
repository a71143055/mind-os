from fastapi import APIRouter
from app.services.graph_store import GraphStore
from app.services.embeddings import DummyEmbeddings

def get_router(graph: GraphStore, embed: DummyEmbeddings) -> APIRouter:
    router = APIRouter(prefix="/agent", tags=["agent"])

    @router.get("/associate")
    def associate(label: str, k: int = 5):
        all_labels = [(n, d.get("label", "")) for n, d in graph.G.nodes(data=True)]
        sims = embed.similar_labels(label, all_labels, k=k)
        return {"query": label, "associations": sims}

    @router.get("/prompt")
    def prompt(current: str):
        # simple inner dialog-style hints
        neighbors = graph.neighbors(current)
        if not neighbors:
            msg = f"'{current}'에서 시작했어. 관련 노드를 추가해볼까?"
        else:
            msg = f"'{current}'와 연상되는 {len(neighbors)}개가 있어. 어떤 걸 확장해볼래?"
        return {"message": msg, "options": neighbors}
    return router
