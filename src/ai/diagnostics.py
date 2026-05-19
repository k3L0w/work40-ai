from __future__ import annotations

import re
from dataclasses import dataclass

from src.utils.config import Settings


SECRET_REDACTION = "[redigido]"


@dataclass(frozen=True)
class SafeAIError:
    safe_error_type: str
    safe_error_message: str


@dataclass(frozen=True)
class AIHealthStatus:
    api_key_present: bool
    chat_available: bool
    embeddings_available: bool
    safe_error_type: str | None = None
    safe_error_message: str | None = None


def check_ai_health(settings: Settings) -> AIHealthStatus:
    """Run minimal online checks and return only sanitized status fields."""
    if not settings.openai_api_key:
        return AIHealthStatus(
            api_key_present=False,
            chat_available=False,
            embeddings_available=False,
        )

    try:
        from openai import OpenAI
    except ImportError as exc:
        safe_error = safe_error_from_exception(exc, settings.openai_api_key)
        return AIHealthStatus(
            api_key_present=True,
            chat_available=False,
            embeddings_available=False,
            safe_error_type=safe_error.safe_error_type,
            safe_error_message=safe_error.safe_error_message,
        )

    try:
        client = OpenAI(api_key=settings.openai_api_key)
    except Exception as exc:
        safe_error = safe_error_from_exception(exc, settings.openai_api_key)
        return AIHealthStatus(
            api_key_present=True,
            chat_available=False,
            embeddings_available=False,
            safe_error_type=safe_error.safe_error_type,
            safe_error_message=safe_error.safe_error_message,
        )

    chat_available, chat_error = _check_chat(client, settings)
    embeddings_available, embeddings_error = _check_embeddings(client, settings)
    safe_error = chat_error or embeddings_error
    return AIHealthStatus(
        api_key_present=True,
        chat_available=chat_available,
        embeddings_available=embeddings_available,
        safe_error_type=safe_error.safe_error_type if safe_error else None,
        safe_error_message=safe_error.safe_error_message if safe_error else None,
    )


def safe_error_from_exception(exc: Exception, *secrets: str | None) -> SafeAIError:
    error_text = sanitize_error_message(str(exc), *secrets).lower()
    error_type = sanitize_error_message(type(exc).__name__, *secrets)

    if any(token in error_text for token in ("quota", "insufficient_quota", "billing")):
        message = "A conta OpenAI não está disponível por limite, quota ou cobrança."
    elif any(token in error_text for token in ("auth", "api key", "unauthorized", "401")):
        message = "A chave de API não foi aceita pelo provedor."
    elif any(token in error_text for token in ("model", "404", "not found")):
        message = "O modelo configurado não está disponível para esta conta."
    elif any(
        token in error_text
        for token in ("network", "timeout", "connection", "dns", "proxy")
    ):
        message = "Não foi possível conectar ao provedor de IA neste momento."
    elif "openai" in error_text and "sdk" in error_text:
        message = "O SDK da OpenAI não está disponível no ambiente."
    else:
        message = "A IA online não pôde ser usada neste momento."

    return SafeAIError(
        safe_error_type=error_type,
        safe_error_message=message,
    )


def sanitize_error_message(message: str, *secrets: str | None) -> str:
    redacted = message
    for secret in secrets:
        if secret:
            redacted = redacted.replace(secret, SECRET_REDACTION)
    redacted = re.sub(r"sk-[A-Za-z0-9_-]{8,}", SECRET_REDACTION, redacted)
    redacted = re.sub(
        r"(OPENAI_API_KEY\s*=\s*)\S+",
        rf"\1{SECRET_REDACTION}",
        redacted,
        flags=re.IGNORECASE,
    )
    return redacted


def _check_chat(client: object, settings: Settings) -> tuple[bool, SafeAIError | None]:
    try:
        response = client.chat.completions.create(
            model=settings.openai_model,
            messages=[
                {
                    "role": "system",
                    "content": "Responda apenas com OK.",
                },
                {"role": "user", "content": "Health check"},
            ],
            temperature=0,
            max_tokens=5,
        )
    except Exception as exc:
        return False, safe_error_from_exception(exc, settings.openai_api_key)

    if not getattr(response, "choices", None):
        return False, SafeAIError(
            safe_error_type="EmptyResponse",
            safe_error_message="A IA online retornou uma resposta vazia.",
        )
    return True, None


def _check_embeddings(
    client: object,
    settings: Settings,
) -> tuple[bool, SafeAIError | None]:
    try:
        response = client.embeddings.create(
            model=settings.openai_embedding_model,
            input=["health check"],
        )
    except Exception as exc:
        return False, safe_error_from_exception(exc, settings.openai_api_key)

    if not getattr(response, "data", None):
        return False, SafeAIError(
            safe_error_type="EmptyEmbeddingResponse",
            safe_error_message="O provedor não retornou embeddings válidos.",
        )
    return True, None
