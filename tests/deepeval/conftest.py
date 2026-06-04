import pytest

from deepeval_tests.models import get_evaluation_model


@pytest.fixture
def evaluation_model():
	return get_evaluation_model()
