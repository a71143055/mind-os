from pydantic import BaseModel
from typing import Dict

class Node(BaseModel):
    id: str
    label: str
    meta: Dict[str, str] = {}

class Edge(BaseModel):
    source: str
    target: str
    weight: float = 1.0
    kind: str = "association"
