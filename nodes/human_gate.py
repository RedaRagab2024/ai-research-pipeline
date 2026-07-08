def human_approval_prompt(state_obj, context_note: str = ""):
    print("\n=== HUMAN VERIFICATION REQUIRED ===")
    if context_note:
        print(context_note)
    bib = state_obj.get("verified_bibliography", []) or []
    print(f"Verified bibliography items: {len(bib)} (sample 5):")
    for b in bib[:5]:
        print(" -", b.get("title") or b.get("doi"))
    while True:
        ans = input("Approve and continue? [y/n]: ").strip().lower()
        if ans in ("y", "yes"):
            state_obj.update("nodes", {"human_gate": {"approved": True}})
            return True
        if ans in ("n", "no"):
            state_obj.update("nodes", {"human_gate": {"approved": False}})
            return False
        print("Please answer y or n.")
