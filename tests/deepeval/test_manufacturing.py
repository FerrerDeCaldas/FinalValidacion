from deepeval import assert_test
from deepeval.test_case import LLMTestCase
from deepeval.metrics import AnswerRelevancyMetric, FaithfulnessMetric, ToxicityMetric

from deepeval_tests.common import load_manufacturing_context


def test_deepeval_manufacturing_functionality(evaluation_model):
	"""
	Evalúa la respuesta de Manufacturing usando Toxicity, Relevancy y Faithfulness.
	"""

	rag_context = [load_manufacturing_context()]

	test_case = LLMTestCase(
		input="¿El proceso de Manufacturing generó el BOM y la orden de trabajo?",
		actual_output=(
			"Sí, el sistema creó el BOM correctamente, calculó los costos y "
			"generó la orden de trabajo en Manufacturing."
		),
		expected_output=(
			"El sistema creó el BOM correctamente, calculó los costos y generó la orden "
			"de trabajo en Manufacturing."
		),
		retrieval_context=rag_context,
	)

	metrics = [
		ToxicityMetric(threshold=0.5, model=evaluation_model),
		AnswerRelevancyMetric(threshold=0.6, model=evaluation_model),
		FaithfulnessMetric(threshold=0.6, model=evaluation_model),
	]

	assert_test(test_case, metrics)
