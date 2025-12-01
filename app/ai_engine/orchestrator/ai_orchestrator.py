"""
Main AI orchestration pipeline.
"""
from typing import Any, Dict, List, Optional

from fastapi import HTTPException, status

from app.ai_engine.agent_assist.suggestion_generator import generate_suggestions
from app.ai_engine.autopilot.autopilot_decider import should_auto_reply
from app.ai_engine.classifiers.intent_classifier import classify_intent
from app.ai_engine.classifiers.sentiment_analyzer import analyze_sentiment
from app.ai_engine.memory.memory_manager import compress_and_store
from app.ai_engine.planner.function_planner import plan_action
from app.ai_engine.providers.provider_selector import chat_completion
from app.ai_engine.rag.query_optimizer import optimize_query
from app.ai_engine.rag.rag_retriever import retrieve_chunks
from app.ai_engine.safety.safety_checker import check_safety
from app.ai_engine.spam_filter.spam_pipeline import is_spam
from app.ai_engine.tuning.ai_settings_loader import load_ai_settings
from app.ai_engine.tuning.prompt_builder import build_prompt
from app.ai_engine.rewriter.tone_rewriter import rewrite_tone
from app.ai_engine.utils.exceptions import SpamDetected
from app.ai_engine.utils.logger import get_logger

logger = get_logger(__name__)


async def run_ai_pipeline(
    org_id: str,
    user_message: str,
    conversation_context: Optional[List[Dict[str, str]]] = None,
    provider: str = "openai",
    metadata: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    try:
        if await is_spam(user_message, metadata, provider):
            raise SpamDetected("Spam detected.")

        intent = await classify_intent(provider, user_message)
        sentiment = await analyze_sentiment(provider, user_message)

        optimized_queries = optimize_query(user_message)
        rag_chunks = retrieve_chunks(org_id, optimized_queries[0], top_k=3)

        settings = load_ai_settings(org_id)
        messages = build_prompt(
            identity="OkeAI Agent",
            persona=settings.get("persona") or "Helpful assistant",
            rules=settings.get("rules") or [],
            style=settings.get("style") or "",
            examples=settings.get("examples") or [],
            rag_chunks=rag_chunks,
            conversation_history=conversation_context,
            safety_rules=[],
            action_mode="normal",
            call_word=settings.get("call_word", ""),
        )
        messages.append({"role": "user", "content": user_message})

        llm_params = settings.get("llm_params") or {}
        llm_result = await chat_completion(provider, messages, llm_params)
        reply = llm_result["content"]

        safety = check_safety(reply)
        if not safety["safe"]:
            reply = "Sorry, I cannot answer that."

        planner = await plan_action(provider, user_message, settings.get("tools", {}))
        action = planner.get("action")

        auto = should_auto_reply(intent=intent.get("intent", ""), org_rules=settings, agent_online=False)

        rewritten = await rewrite_tone(provider, reply, settings.get("persona", ""), settings.get("style", ""))
        suggestions = await generate_suggestions(provider, user_message)

        return {
            "reply": rewritten,
            "action": planner if action else None,
            "classification": intent,
            "sentiment": sentiment.get("sentiment"),
            "rag_used": bool(rag_chunks),
            "should_auto_reply": auto.get("should_auto_reply"),
            "safety": safety,
            "suggestions": suggestions,
        }
    except SpamDetected as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"code": "ERR_SPAM", "message": str(exc)},
        )
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("AI pipeline failed")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"code": "ERR_AI_PIPELINE", "message": "AI pipeline failed."},
        ) from exc
