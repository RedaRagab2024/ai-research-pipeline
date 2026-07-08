# AI Research Pipeline

This repository contains a modular, graph-based AI-assisted research pipeline for building reproducible, multi-agent systematic reviews.

Features
- Graph-based orchestrator (nodes) for Librarian, Reviewer, Writer, QA, and Human Gate
- PubMed (Entrez) integration with Crossref DOI verification
- Citation Contract enforced at Writer node (LLM wrapper example for OpenAI)
- FastAPI-based minimal Human-in-the-loop gate (web UI)
- Shared state, PRISMA checklist skeleton, CI/test skeleton

Placeholders & secrets
- Do NOT commit API keys. This repo uses environment variables (placeholders listed below). Set them as GitHub Secrets for CI or in a local .env file for local runs.

Required environment variables (placeholders):
- ENTREZ_EMAIL
- OPENAI_API_KEY
- CROSSREF_EMAIL (optional)
- GRAMMARLY_KEY (optional)
- SERPER_KEY (optional)

Quickstart (local)
1. Create and activate a Python virtualenv
2. pip install -r requirements.txt
3. Set environment variables (ENTREZ_EMAIL, OPENAI_API_KEY)
4. Run a quick pipeline demo: python orchestrator.py
5. Run the web UI: uvicorn webui.app:app --reload

See the individual node files for implementation details, usage notes, and rate-limit guidance.
