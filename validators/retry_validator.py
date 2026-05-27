"""
Pydantic-based validation with retry and fallback for LLM extractions.
"""
from __future__ import annotations
import json
import re
from typing import Type, TypeVar
from pydantic import BaseModel, ValidationError
import anthropic

T = TypeVar("T", bound=BaseModel)


def clean_json(text: str) -> str:
    text = text.strip()
    text = re.sub(r"^```(?:json)?\n?", "", text)
    text = re.sub(r"\n?```$", "", text)
    return text.strip()


def extract_with_retry(
    text: str,
    output_model: Type[T],
    model: str = "claude-sonnet-4-20250514",
    max_retries: int = 3,
) -> T:
    client = anthropic.Anthropic()
    schema = json.dumps(output_model.model_json_schema(), indent=2)
    history = []

    for attempt in range(max_retries):
        prompt = f"Extract structured data from this text and return ONLY valid JSON matching this schema:\n{schema}\n\nText: {text}"
        if history:
            prompt += f"\n\nPrevious attempt failed with: {history[-1]}. Fix the JSON."

        resp = client.messages.create(
            model=model, max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )
        raw = clean_json(resp.content[0].text)
        try:
            data = json.loads(raw)
            return output_model(**data)
        except (json.JSONDecodeError, ValidationError) as e:
            history.append(str(e))
            if attempt == max_retries - 1:
                raise ValueError(f"Extraction failed after {max_retries} attempts. Last error: {e}")
