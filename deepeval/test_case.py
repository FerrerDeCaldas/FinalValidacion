from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class LLMTestCase:
	input: str
	actual_output: str
	expected_output: str | None = None
	retrieval_context: list[Any] | None = None
