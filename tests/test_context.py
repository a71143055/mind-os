from app.services.context_manager import ContextManager

def test_context_push_pop():
    ctx = ContextManager(initial_focus="home")
    ctx.push("ideas")
    ctx.push("travel")
    assert ctx.current().focus_node == "travel"
    back = ctx.pop()
    assert back == "ideas"
    back2 = ctx.pop()
    assert back2 == "home"
