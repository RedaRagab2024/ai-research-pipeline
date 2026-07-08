import networkx as nx
from state import state
from nodes import librarian, reviewer, writer, qa, human_gate

def build_graph():
    G = nx.DiGraph()
    G.add_node("librarian", func=librarian.run)
    G.add_node("reviewer", func=reviewer.run)
    G.add_node("writer", func=writer.draft_section)
    G.add_node("qa", func=qa.run)
    G.add_node("human_gate", func=human_gate.human_approval_prompt)
    G.add_edge("librarian", "reviewer")
    G.add_edge("reviewer", "human_gate")
    G.add_edge("human_gate", "writer")
    G.add_edge("writer", "qa")
    return G

def run_pipeline(query: str, sections: list):
    state.set("query", query)
    G = build_graph()
    print("[orchestrator] Running librarian...")
    G.nodes["librarian"]["func"](state, query)
    print("[orchestrator] Running reviewer (PRISMA checks)...")
    G.nodes["reviewer"]["func"](state)
    print("[orchestrator] Human verification required before drafting.")
    ok = G.nodes["human_gate"]["func"](state, "Please review the PRISMA checklist and bibliography before drafting.")
    if not ok:
        print("Human rejected. Halting pipeline.")
        return
    print("[orchestrator] Human approved. Drafting sections...")
    for sec in sections:
        G.nodes["writer"]["func"](state, sec, f"Write section {sec}")
    print("[orchestrator] Running QA...")
    report = G.nodes["qa"]["func"](state)
    print("QA report generated.")
    return report

if __name__ == "__main__":
    run_pipeline("machine learning bias systematic review", ["introduction", "methods", "results", "discussion"])
