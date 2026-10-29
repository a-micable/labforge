# thin wrapper around Token Factory's openai-compatible chat API

from __future__ import annotations

import os
from typing import Any

from openai import OpenAI

DEFAULT_BASE_URL = "https://api.tokenfactory.nebius.com/v1/"
# nano is enough for the RC / beamforming tasks; bump via env if needed
DEFAULT_MODEL = "nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B"


def get_client() -> OpenAI:
    key = os.environ.get("NEBIUS_API_KEY", "").strip()
    if not key:
        raise RuntimeError(
            "NEBIUS_API_KEY missing — create one in Token Factory and put it in .env"
        )
    return OpenAI(
        base_url=os.environ.get("NEBIUS_BASE_URL", DEFAULT_BASE_URL).strip(),
        api_key=key,
    )


def get_model() -> str:
    return os.environ.get("NEBIUS_MODEL", DEFAULT_MODEL).strip()


def chat(
    messages: list[dict[str, str]],
    *,
    temperature: float = 0.2,
    max_tokens: int = 4096,
) -> str:
    resp = get_client().chat.completions.create(
        model=get_model(),
        messages=messages,  # type: ignore[arg-type]
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return (resp.choices[0].message.content or "").strip()


def describe_stack() -> dict[str, Any]:
    return {
        "provider": "Nebius Token Factory",
        "base_url": os.environ.get("NEBIUS_BASE_URL", DEFAULT_BASE_URL),
        "model": get_model(),
        "nvidia_open_model": True,
        "api_key_configured": bool(os.environ.get("NEBIUS_API_KEY", "").strip()),
    }
