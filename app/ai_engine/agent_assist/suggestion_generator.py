"""
Generate agent assist suggestions.
"""
from typing import List

from app.ai_engine.providers.provider_selector import chat_completion

PROMPT = """
Provide 3 concise reply suggestions for the agent. Return them as bullet lines.
"""


async def generate_suggestions(provider: str, message: str) -> List[str]:
    messages = [{"role": "system", "content": PROMPT}, {"role": "user", "content": message}]
    result = await chat_completion(provider, messages, {"temperature": 0.5, "max_tokens": 128})
    lines = [line.strip("- ").strip() for line in result["content"].splitlines() if line.strip()]
    return [line for line in lines if line][:3]
