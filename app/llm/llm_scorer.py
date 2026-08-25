"""
Phase 3 stretch goal — NOT wired into /score yet.

Rather than training a classifier (no dataset yet — see README precondition),
this uses few-shot prompting against an LLM: give it a handful of labeled
examples inline and ask it to score + explain the new message. This is
honest to demo (you can show judges exactly what's in the prompt) and needs
no training pipeline.

To activate:
  1. Set AI_SERVICE_LLM_ENABLED=true
  2. Wire this into main.py as a secondary field on ScoreResponse
     (e.g. `llm_opinion`), never as a silent replacement for the rule engine.
     Keep both visible — if they disagree, that disagreement is itself
     useful signal to show the user, not something to hide.
"""

import json
import os

FEW_SHOT_EXAMPLES = [
    {"message": "Pay Rs 499 registration fee to confirm your work from home job.", "label": "scam"},
    {"message": "Please join the technical interview on Google Meet at 3 PM tomorrow.", "label": "legit"},
    {"message": "Dear Candidate, selected without interview. Send Aadhar card immediately.", "label": "scam"},
]

SYSTEM_PROMPT = """You are a fraud-detection assistant reviewing internship/job offer \
messages sent to college students in India. You are given a new message and must \
respond ONLY with JSON: {"opinion": "scam"|"legit"|"unclear", "confidence": 0-100, \
"reasoning": "one sentence"}. Do not add any other text."""


def build_prompt(message: str) -> str:
    examples_text = "\n".join(
        f'Example: "{ex["message"]}" -> {ex["label"]}' for ex in FEW_SHOT_EXAMPLES
    )
    return f"{examples_text}\n\nNew message: \"{message}\"\n\nRespond with the JSON only."


def llm_enabled() -> bool:
    return os.environ.get("AI_SERVICE_LLM_ENABLED", "false").lower() == "true"


def get_llm_opinion(message: str) -> dict:
    """
    Placeholder — wire to your actual LLM API client here (Anthropic API,
    etc.) once you're ready for Phase 3. Left unimplemented on purpose so
    it fails loudly instead of silently returning fake confidence numbers.
    """
    if not llm_enabled():
        raise RuntimeError(
            "LLM scoring is disabled. Set AI_SERVICE_LLM_ENABLED=true and "
            "implement the API call in get_llm_opinion() before using this."
        )
    raise NotImplementedError(
        "Wire this up to your LLM client. Use build_prompt(message) and "
        "SYSTEM_PROMPT, then json.loads() the response — don't skip the "
        "try/except, the model can occasionally return malformed JSON."
    )
