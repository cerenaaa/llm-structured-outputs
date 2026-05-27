# LLM Structured Outputs

[![CI](https://github.com/cerenaaa/llm-structured-outputs/actions/workflows/ci.yml/badge.svg)](https://github.com/cerenaaa/llm-structured-outputs/actions)

Reliable structured JSON extraction from LLMs. Uses Claude's tool-use API for guaranteed schema compliance, with Pydantic validation, retry logic, and fallback parsing.

## The problem

Raw LLM output is unpredictable. Even with "return JSON only" instructions, models add markdown fences, miss fields, or return invalid types. This library makes structured extraction reliable.

## Approaches

| Method | Reliability | Flexibility |
|---|---|---|
| Tool use (function calling) | ★★★★★ | Schema-bound |
| Pydantic + retry | ★★★★ | Flexible |
| Regex fallback | ★★★ | Simple fields only |

## Quickstart
```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=your_key
python extract.py
```

## Example
```python
from extractors.tool_extractor import extract
from schemas.common import SentimentResult

result = extract("This product is fantastic!", SentimentResult)
# SentimentResult(label='positive', score=0.92, reasoning='...')
```
