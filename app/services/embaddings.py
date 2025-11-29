# Placeholder for semantic embeddings (optional extension).
# Keeps interface so later you can plug real models.
from typing import List, Tuple

class DummyEmbeddings:
    def __init__(self):
        pass

    def similar_labels(self, label: str, all_labels: List[Tuple[str, str]], k: int = 5):
        # naive: substring overlap score
        q = set(label.lower().split())
        scored = []
        for node_id, node_label in all_labels:
            tokens = set(node_label.lower().split())
            score = len(q & tokens)
            scored.append((node_id, float(score)))
        scored.sort(key=lambda x: x[1], reverse=True)
        return [s for s in scored if s[1] > 0][:k]
