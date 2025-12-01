def test_import_ai_engine_modules():
    import app.ai_engine.providers.provider_selector as provider_selector  # noqa: F401
    import app.ai_engine.tuning.prompt_builder as prompt_builder  # noqa: F401
    import app.ai_engine.orchestrator.ai_orchestrator as orchestrator  # noqa: F401
