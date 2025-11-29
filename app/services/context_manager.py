from app.models.context import ContextState

class ContextManager:
    def __init__(self, initial_focus: str = "home"):
        self.state = ContextState(focus_node=initial_focus, stack=[], timeline=[])

    def push(self, node_id: str):
        if self.state.focus_node != node_id:
            self.state.stack.append(self.state.focus_node)
            self.state.timeline.append(node_id)
            self.state.focus_node = node_id

    def pop(self) -> str:
        if self.state.stack:
            self.state.focus_node = self.state.stack.pop()
        return self.state.focus_node

    def reset(self, node_id: str = "home"):
        self.state = ContextState(focus_node=node_id, stack=[], timeline=[])

    def current(self) -> ContextState:
        return self.state
