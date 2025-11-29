async function api(path, opts = {}) {
    const res = await fetch(path, {
        headers: { "Content-Type": "application/json" },
        ...opts
    });
    if (res.headers.get("content-type")?.includes("application/json")) {
        return res.json();
    }
    return res.text();
}

function setFocus(name) {
    document.getElementById("focus-node").innerText = name;
}

async function refreshContext() {
    const s = await api("/context/state");
    setFocus(s.focus);
    const sugEl = document.getElementById("suggestions");
    sugEl.innerHTML = "";
    const sug = await api(`/context/focus/${s.focus}`, { method: "POST" });
    setFocus(sug.focus);
    sugEl.innerHTML = "";
    sug.suggestions.forEach(([nid, w]) => {
        const li = document.createElement("li");
        li.innerHTML = `<strong>${nid}</strong> (w=${w})`;
        li.onclick = () => focusNode(nid);
        sugEl.appendChild(li);
    });
    const tlEl = document.getElementById("timeline");
    tlEl.innerHTML = "";
    (s.timeline || []).forEach(n => {
        const li = document.createElement("li");
        li.textContent = n;
        tlEl.appendChild(li);
    });
}

async function focusNode(nodeId) {
    const r = await api(`/context/focus/${nodeId}`, { method: "POST" });
    setFocus(r.focus);
    const sugEl = document.getElementById("suggestions");
    sugEl.innerHTML = "";
    r.suggestions.forEach(([nid, w]) => {
        const li = document.createElement("li");
        li.innerHTML = `<strong>${nid}</strong> (w=${w})`;
        li.onclick = () => focusNode(nid);
        sugEl.appendChild(li);
    });
    const tlEl = document.getElementById("timeline");
    tlEl.innerHTML = "";
    r.timeline.forEach(n => {
        const li = document.createElement("li");
        li.textContent = n;
        tlEl.appendChild(li);
    });
}

document.getElementById("search-btn").onclick = async () => {
    const q = document.getElementById("search-input").value;
    const r = await api(`/graph/search?q=${encodeURIComponent(q)}`);
    const list = document.getElementById("search-results");
    list.innerHTML = "";
    r.results.forEach(item => {
        const li = document.createElement("li");
        li.innerHTML = `<strong>${item.id}</strong> — ${item.label}`;
        li.onclick = () => focusNode(item.id);
        list.appendChild(li);
    });
};

document.getElementById("add-node-btn").onclick = async () => {
    const id = document.getElementById("node-id").value.trim();
    const label = document.getElementById("node-label").value.trim();
    if (!id || !label) return;
    await api("/graph/node", { method: "POST", body: JSON.stringify({ id, label, meta: {} }) });
    await focusNode(id);
};

document.getElementById("add-edge-btn").onclick = async () => {
    const source = document.getElementById("edge-src").value.trim();
    const target = document.getElementById("edge-tgt").value.trim();
    if (!source || !target) return;
    await api("/graph/edge", { method: "POST", body: JSON.stringify({ source, target, weight: 1.0, kind: "association" }) });
    await focusNode(source);
};

document.getElementById("back-btn").onclick = async () => {
    const r = await api("/context/back", { method: "POST" });
    setFocus(r.focus);
    const sugEl = document.getElementById("suggestions");
    sugEl.innerHTML = "";
    r.suggestions.forEach(([nid, w]) => {
        const li = document.createElement("li");
        li.innerHTML = `<strong>${nid}</strong> (w=${w})`;
        li.onclick = () => focusNode(nid);
        sugEl.appendChild(li);
    });
    const tlEl = document.getElementById("timeline");
    tlEl.innerHTML = "";
    r.timeline.forEach(n => {
        const li = document.createElement("li");
        li.textContent = n;
        tlEl.appendChild(li);
    });
};

document.getElementById("reset-btn").onclick = async () => {
    const r = await api("/context/reset", { method: "POST" });
    setFocus(r.focus);
    await refreshContext();
};

document.getElementById("assoc-btn").onclick = async () => {
    const label = document.getElementById("assoc-input").value.trim();
    if (!label) return;
    const r = await api(`/agent/associate?label=${encodeURIComponent(label)}`);
    const list = document.getElementById("assoc-results");
    list.innerHTML = "";
    r.associations.forEach(([nid, score]) => {
        const li = document.createElement("li");
        li.innerHTML = `<strong>${nid}</strong> (score=${score})`;
        li.onclick = () => focusNode(nid);
        list.appendChild(li);
    });
};

window.addEventListener("load", async () => {
    await refreshContext();
});
