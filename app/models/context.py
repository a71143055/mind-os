from pydantic import BaseModel
from typing import List

class ContextState(BaseModel):
    focus_node: str
    stack: List[str] = []
    timeline: List[str] = []
