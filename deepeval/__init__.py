from .test_case import LLMTestCase
from .metrics import AnswerRelevancyMetric, FaithfulnessMetric, ToxicityMetric


def assert_test(test_case: LLMTestCase, metrics: list[object]) -> None:
	failed = []
	for metric in metrics:
		score = metric.evaluate(test_case)
		if score < metric.threshold:
			failed.append(
				f"{type(metric).__name__} failed: score={score:.2f}, "
				f"threshold={metric.threshold}"
			)
	if failed:
		raise AssertionError("\n".join(failed))

__all__ = [
	"assert_test",
	"LLMTestCase",
	"ToxicityMetric",
	"AnswerRelevancyMetric",
	"FaithfulnessMetric",
]
