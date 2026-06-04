# DeepEval para el proyecto

Este directorio contiene pruebas de evaluación automática para las respuestas del agente usando `deepeval`.

## Qué incluye

- `tests/deepeval/test_toxicity.py` - prueba de toxicidad
- `tests/deepeval/test_rag_login.py` - prueba de relevancia y fidelidad con contexto RAG
- `tests/deepeval/test_manufacturing.py` - prueba de Manufacturing
- `tests/deepeval/test_quality_management.py` - prueba de Quality Management
- `tests/deepeval/test_shopping_cart.py` - prueba de Shopping Cart

## Cómo ejecutar

Desde el directorio raíz del repositorio:

```powershell
pip install -r requirements-test.txt
python -m pytest tests/deepeval
```

## Notas

- La biblioteca `deepeval` está implementada como un paquete local bajo `deepeval/`.
- Asegúrate de no tener un paquete Python llamado `tests/deepeval` en el árbol de importación del proyecto.
- Los tests usan el package local `deepeval_tests` para datos de soporte y modelos de evaluación.
