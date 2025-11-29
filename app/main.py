from fastapi import FastAPI
from fastapi.responses import FileResponse
from pathlib import Path
from app.services.graph_store import GraphStore
from app.services.context_manager import ContextManager
from app.services.recommender import Recommender
from app.services.persistence import Persistence
from app.services.embeddings import DummyEmbeddings
from app.routes.graph import get_router as graph_router_factory
from app.routes.context import get_router as context_router_factory
from app.routes.agent import get_router as agent_router_factory

app = FastAPI(title="MindOS")

# core services
graph = GraphStore()
ctx = ContextManager(initial_focus="home")
rec = Recommender(graph)
embed = DummyEmbeddings()
store = Persistence()

# preload from DB
for n in store.load_nodes():
    graph.ensure_node(n["id"], n["label"])
for e in store.load_edges():
    graph.add_edge(type("E", (), e)())  # quick obj with attrs

# default seed
graph.ensure_node("home", "Home")
graph.ensure_node("ideas", "Ideas")
graph.ensure_node("travel", "Travel")
graph.ensure_node("work", "Work")
graph.add_edge(type("E", (), {"source": "home", "target": "ideas", "weight": 1.0, "kind": "association"})())
graph.add_edge(type("E", (), {"source": "home", "target": "work", "weight": 0.8, "kind": "association"})())
graph.add_edge(type("E", (), {"source": "ideas", "target": "travel", "weight": 0.9, "kind": "association"})())

# routes
app.include_router(graph_router_factory(graph))
app.include_router(context_router_factory(ctx, rec))
app.include_router(agent_router_factory(graph, embed))

# static UI
UI_DIR = Path(__file__).parent / "ui" / "web"

@app.get("/")
def index():
    return FileResponse(str(UI_DIR / "index.html"))

@app.get("/web/{asset}")
def assets(asset: str):
    path = UI_DIR / asset
    if path.exists():
        return FileResponse(str(path))
    return {"error": "not found"}

@app.on_event("shutdown")
def persist_all():
    nodes = [{"id": nid, "label": data.get("label"), "meta": data.get("meta", {})}
             for nid, data in graph.G.nodes(data=True)]
    edges = []
    for u, v, d in graph.G.edges(data=True):
        edges.append({"source": u, "target": v, "weight": d.get("weight", 1.0), "kind": d.get("kind", "association")})
    store.save_nodes(nodes)
    store.save_edges(edges)
