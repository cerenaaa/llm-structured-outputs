"""
Tool-use based structured extraction.
Uses Anthropic function calling for guaranteed JSON schema compliance.
"""
from __future__ import annotations
import json
from typing import Type, TypeVar
from pydantic import BaseModel
import anthropic

T = TypeVar("T", bound=BaseModel)


def _schema_to_tool(model: Type[BaseModel]) -> dict:
    schema = model.model_json_schema()
    return {
        "name": "extract_structured_data",
        "description": f"Extract structured {model.__name__} from the provided text",
        "input_schema": {
            "type": "object",
            "properties": schema.get("properties", {}),
            "required": schema.get("required", []),
        }
    }


def extract(
    text: str,
    output_model: Type[T],
    model: str = "claude-sonnet-4-20250514",
    system: str = "Extract the requested information accurately from the text.",
    max_retries: int = 2,
) -> T:
    client = anthropic.Anthropic()
    tool = _schema_to_tool(output_model)

    for attempt in range(max_retries + 1):
        resp = client.messages.create(
            model=model, max_tokens=1024,
            system=system,
            tools=[tool],
            tool_choice={"type": "tool", "name": "extract_structured_data"},
            messages=[{"role": "user", "content": text}],
        )
        for block in resp.content:
            if block.type == "tool_use":
                return output_model(**block.input)
    raise ValueError(f"Extraction failed after {max_retries + 1} attempts")


def extract_batch(
    texts: list[str],
    output_model: Type[T],
    **kwargs,
) -> list[T | None]:
    results = []
    for text in texts:
        try:
            results.append(extract(text, output_model, **kwargs))
        except Exception as e:
            print(f"  Extraction failed: {e}")
            results.append(None)
    return results
