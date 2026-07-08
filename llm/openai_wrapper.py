import os
import openai
import re
from typing import List, Dict

openai_api_key = os.getenv("OPENAI_API_KEY")
if openai_api_key:
    openai.api_key = openai_api_key

CITATION_PATTERN = re.compile(r"\[doi:([^\]]+)\]")

def call_llm(system_prompt: str, user_prompt: str, allowed_dois: List[str]) -> Dict:
    """Call OpenAI ChatCompletion and enforce the Citation Contract by post-checking citations.

    - system_prompt: high-level instruction
    - user_prompt: the section prompt + allowed DOIs
    - allowed_dois: list of DOIs the model is allowed to cite

    Returns: {"text": str, "citations_valid": bool, "invalid_citations": []}
    """
    if not openai_api_key:
        # Fallback: return a placeholder draft
        text = f"(LLM disabled) Draft for prompt: {user_prompt}\n\nAllowed DOIs: {allowed_dois}"
        return {"text": text, "citations_valid": True, "invalid_citations": []}

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]
    resp = openai.ChatCompletion.create(model="gpt-4o-mini", messages=messages, temperature=0.2)
    text = resp.choices[0].message.content
    found = CITATION_PATTERN.findall(text)
    invalid = [d for d in found if d not in allowed_dois]
    return {"text": text, "citations_valid": len(invalid) == 0, "invalid_citations": invalid}
