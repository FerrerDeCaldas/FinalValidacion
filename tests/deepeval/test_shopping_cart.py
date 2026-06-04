from deepeval import assert_test
from deepeval.test_case import LLMTestCase
from deepeval.metrics import AnswerRelevancyMetric, FaithfulnessMetric, ToxicityMetric

from deepeval_tests.common import load_shopping_cart_context


def test_deepeval_shopping_cart_functionality(evaluation_model):
	"""
	Evalúa la respuesta de Shopping Cart usando Toxicity, Relevancy y Faithfulness.
	"""

	rag_context = [load_shopping_cart_context()]

	test_case = LLMTestCase(
		input="¿El carrito calculó correctamente descuentos e impuestos?",
		actual_output=(
			"El Shopping Cart calculó el subtotal, aplicó descuentos y sumó el impuesto "
			"correctamente para obtener el total final."
		),
		expected_output=(
			"El Shopping Cart calculó el subtotal, aplicó descuentos y sumó el impuesto "
			"correctamente para obtener el total final."
		),
		retrieval_context=rag_context,
	)

	metrics = [
		ToxicityMetric(threshold=0.5, model=evaluation_model),
		AnswerRelevancyMetric(threshold=0.6, model=evaluation_model),
		FaithfulnessMetric(threshold=0.6, model=evaluation_model),
	]

	assert_test(test_case, metrics)
