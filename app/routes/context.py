from fastapi import APIRouter
from app.services.context_manager import ContextManager
from app.services.recommender import Recommender

def get_router(ctx: ContextManager, rec: Recommender) -> APIRouter:
    router = APIRouter(prefix="/context", tags=["context"])

    @router.post("/focus/{node_id}")
    def focus(node_id: str):
        ctx.push(node_id)
        suggestions = rec.suggest_next(node_id)
        return {"focus": ctx.current().focus_node, "suggestions": suggestions, "timeline": ctx.current().timeline}

    @router.post("/back")
    def back():
        focus = ctx.pop()
        suggestions = rec.suggest_next(focus)
        return {"focus": focus, "suggestions": suggestions, "timeline": ctx.current().timeline}

    @router.post("/reset")
    def reset(node_id: str = "home"):
        ctx.reset(node_id)
        return {"focus": ctx.current().focus_node, "timeline": ctx.current().timeline}

    @router.get("/state")
    def state():
        s = ctx.current()
        return {"focus": s.focus_node, "stack": s.stack, "timeline": s.timeline}

    return router
