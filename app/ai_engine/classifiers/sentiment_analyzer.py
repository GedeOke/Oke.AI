"""
Sentiment analyzer using LLM prompt.
"""
from typing import Dict

from app.ai_engine.providers.provider_selector import chat_completion
from app.ai_engine.utils.logger import get_logger

logger = get_logger(__name__)

SENTIMENT_PROMPT = """
Analyze sentiment of the following text. Respond with JSON: {"sentiment": "positive|neutral|negative"}.
"""


async def analyze_sentiment(provider: str, message: str) -> Dict[str, str]:
    messages = [{"role": "system", "content": SENTIMENT_PROMPT}, {"role": "user", "content": message}]
    result = await chat_completion(provider, messages, {"temperature": 0.0, "max_tokens": 32})
    return {"sentiment": result["content"]}
