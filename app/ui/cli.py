import typer
from rich.table import Table
from rich.console import Console
import requests

app = typer.Typer()
console = Console()
BASE = "http://localhost:8000"

@app.command()
def focus(node_id: str):
    r = requests.post(f"{BASE}/context/focus/{node_id}")
    data = r.json()
    console.print(f"[bold]Focus:[/bold] {data['focus']}")
    t = Table(title="Suggestions")
    t.add_column("Node")
    t.add_column("Weight")
    for nid, w in data["suggestions"]:
        t.add_row(nid, str(w))
    console.print(t)

@app.command()
def back():
    r = requests.post(f"{BASE}/context/back")
    console.print(r.json())

@app.command()
def add_node(id: str, label: str):
    r = requests.post(f"{BASE}/graph/node", json={"id": id, "label": label, "meta": {}})
    console.print(r.json())

@app.command()
def add_edge(source: str, target: str, weight: float = 1.0):
    r = requests.post(f"{BASE}/graph/edge", json={"source": source, "target": target, "weight": weight, "kind": "association"})
    console.print(r.json())

@app.command()
def search(q: str):
    r = requests.get(f"{BASE}/graph/search", params={"q": q})
    data = r.json()
    t = Table(title=f"Search: {q}")
    t.add_column("ID")
    t.add_column("Label")
    for item in data["results"]:
        t.add_row(item["id"], item["label"])
    console.print(t)

if __name__ == "__main__":
    app()
