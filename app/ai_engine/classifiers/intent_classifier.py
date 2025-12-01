"""
Intent classifier using LLM prompt.
"""
from typing import Dict

from app.ai_engine.providers.provider_selector import chat_completion
from app.ai_engine.utils.logger import get_logger

logger = get_logger(__name__)


INTENT_PROMPT = """
Classify the user's intent. Respond with JSON: {"intent": "<intent>"}.
"""


async def classify_intent(provider: str, message: str) -> Dict[str, str]:
    messages = [{"role": "system", "content": INTENT_PROMPT}, {"role": "user", "content": message}]
    result = await chat_completion(provider, messages, {"temperature": 0.0, "max_tokens": 64})
    return {"intent": result["content"]}
