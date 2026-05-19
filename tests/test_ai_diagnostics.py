import sys
from types import SimpleNamespace

from src.ai.diagnostics import check_ai_health, safe_error_from_exception
from src.utils.config import Settings


class _SuccessfulCompletions:
    def create(self, **_kwargs: object) -> object:
        return SimpleNamespace(
            choices=[SimpleNamespace(message=SimpleNamespace(content="OK"))]
        )


class _SuccessfulEmbeddings:
    def create(self, **_kwargs: object) -> object:
        return SimpleNamespace(data=[SimpleNamespace(embedding=[1.0, 0.0])])


class _SuccessfulOpenAIClient:
    def __init__(self, api_key: str | None) -> None:
        self.chat = SimpleNamespace(completions=_SuccessfulCompletions())
        self.embeddings = _SuccessfulEmbeddings()


class _FailingCompletions:
    def create(self, **_kwargs: object) -> object:
        raise RuntimeError("quota exceeded for sk-test-secret-123456789")


class _FailingEmbeddings:
    def create(self, **_kwargs: object) -> object:
        raise RuntimeError("network unavailable for sk-test-secret-123456789")


class _FailingOpenAIClient:
    def __init__(self, api_key: str | None) -> None:
        self.chat = SimpleNamespace(completions=_FailingCompletions())
        self.embeddings = _FailingEmbeddings()


def _settings(api_key: str | None = "sk-test-secret-123456789") -> Settings:
    return Settings(
        openai_api_key=api_key,
        openai_model="test-chat-model",
        app_env="test",
        openai_embedding_model="test-embedding-model",
    )


def test_ai_health_reports_offline_without_api_key() -> None:
    health = check_ai_health(_settings(api_key=None))

    assert health.api_key_present is False
    assert health.chat_available is False
    assert health.embeddings_available is False
    assert health.safe_error_type is None
    assert health.safe_error_message is None


def test_ai_health_reports_chat_and_embeddings_available(monkeypatch) -> None:
    monkeypatch.setitem(
        sys.modules,
        "openai",
        SimpleNamespace(OpenAI=_SuccessfulOpenAIClient),
    )

    health = check_ai_health(_settings())

    assert health.api_key_present is True
    assert health.chat_available is True
    assert health.embeddings_available is True
    assert health.safe_error_type is None
    assert health.safe_error_message is None


def test_ai_health_reports_safe_failure_without_exposing_secret(monkeypatch) -> None:
    monkeypatch.setitem(
        sys.modules,
        "openai",
        SimpleNamespace(OpenAI=_FailingOpenAIClient),
    )

    health = check_ai_health(_settings())

    assert health.api_key_present is True
    assert health.chat_available is False
    assert health.embeddings_available is False
    assert health.safe_error_type == "RuntimeError"
    assert health.safe_error_message
    assert "sk-test-secret" not in health.safe_error_message


def test_safe_error_does_not_expose_secrets() -> None:
    safe_error = safe_error_from_exception(
        RuntimeError("bad key sk-test-secret-123456789 OPENAI_API_KEY=sk-other-secret"),
        "sk-test-secret-123456789",
    )

    assert safe_error.safe_error_type == "RuntimeError"
    assert "sk-test-secret" not in safe_error.safe_error_message
    assert "sk-other-secret" not in safe_error.safe_error_message
