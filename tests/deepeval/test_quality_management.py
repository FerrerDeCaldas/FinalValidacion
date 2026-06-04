from deepeval import assert_test
from deepeval.test_case import LLMTestCase
from deepeval.metrics import AnswerRelevancyMetric, FaithfulnessMetric, ToxicityMetric

from deepeval_tests.common import load_quality_management_context


def test_deepeval_quality_management_functionality(evaluation_model):
	"""
	Evalúa la respuesta de Quality Management usando Toxicity, Relevancy y Faithfulness.
	"""

	rag_context = [load_quality_management_context()]

	test_case = LLMTestCase(
		input="¿La revisión de calidad fue aprobada y se creó la acción correctiva?",
		actual_output=(
			"La revisión de Quality Management se aprobó, se registró la acción "
			"correctiva y se vinculó al procedimiento de calidad."
		),
		expected_output=(
			"La revisión de Quality Management se aprobó, se registró la acción "
			"correctiva y se vinculó al procedimiento de calidad."
		),
		retrieval_context=rag_context,
	)

	metrics = [
		ToxicityMetric(threshold=0.5, model=evaluation_model),
		AnswerRelevancyMetric(threshold=0.6, model=evaluation_model),
		FaithfulnessMetric(threshold=0.6, model=evaluation_model),
	]

	assert_test(test_case, metrics)
