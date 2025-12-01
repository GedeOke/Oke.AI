"""
Summarization helper using LLM.
"""
from typing import List

from app.ai_engine.providers.provider_selector import chat_completion

SUMMARY_PROMPT = "Summarize the following conversation succinctly."


async def summarize(provider: str, conversation: List[dict]) -> str:
    messages = [{"role": "system", "content": SUMMARY_PROMPT}] + conversation
    result = await chat_completion(provider, messages, {"temperature": 0.2, "max_tokens": 128})
    return result["content"]
