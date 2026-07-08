from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
import uvicorn
from state import state

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def home():
    bib = state.get("verified_bibliography", []) or []
    draft = state.get("working_draft", {}) or {}
    html = f"<h1>Human Gate</h1><p>Verified bibliography: {len(bib)}</p><p>Draft sections: {len(draft)}</p>"
    html += "<form method='post' action='/approve'><button type='submit'>Approve</button></form>"
    html += "<form method='post' action='/reject'><button type='submit'>Reject</button></form>"
    return html

@app.post("/approve")
async def approve():
    state.update("nodes", {"human_gate": {"approved": True}})
    return HTMLResponse("<p>Approved. You can close this window.</p>")

@app.post("/reject")
async def reject():
    state.update("nodes", {"human_gate": {"approved": False}})
    return HTMLResponse("<p>Rejected. You can close this window.</p>")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
