from typing import Dict, Any
from state import state

PRISMA_ITEMS = [
    "title", "abstract", "introduction", "eligibility_criteria",
    "information_sources", "search_strategy", "selection_process",
    "data_collection", "risk_of_bias", "synthesis_methods", "certainty"
]

def check_prisma(state_obj):
    draft = state_obj.get("working_draft", {}) or {}
    prisma_status = state_obj.get("prisma", {}) or {}
    for item in PRISMA_ITEMS:
        prisma_status[item] = bool(draft.get(item))
    state_obj.set("prisma", prisma_status)
    state_obj.update("nodes", {"reviewer": {"prisma_completed": True}})
    return prisma_status

def run(state_obj):
    return check_prisma(state_obj)
