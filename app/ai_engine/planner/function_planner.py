"""
Function calling planner.
"""
from typing import Any, Dict

from app.ai_engine.providers.provider_selector import chat_completion

PROMPT = """
Decide if a function call is needed. Respond with JSON:
{"action": "<function_name or null>", "arguments": {...}}
"""


async def plan_action(provider: str, message: str, tools_schema: Dict[str, Any]) -> Dict[str, Any]:
    messages = [{"role": "system", "content": PROMPT}, {"role": "user", "content": message}]
    result = await chat_completion(provider, messages, {"temperature": 0.0, "max_tokens": 128})
    return {"action": None, "arguments": {}, "raw": result["content"]}
