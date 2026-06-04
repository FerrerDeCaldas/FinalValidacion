# Stagehand - Manufacturing

## Objetivo
Crear un plan de pruebas para el módulo `manufacturing` de ERPNext, con foco en BOM, Work Order, Production Planning y estaciones de trabajo.

## Alcance
- Crear y validar listas de materiales (BOM)
- Verificar cantidades y costos
- Generar órdenes de trabajo
- Actualizar estados y cantidades en Work Orders
- Simular planificación de producción con estaciones de trabajo

## Casos de prueba
1. **Crear BOM exitosamente**
   - Validar creación de BOM con varios items
   - Verificar cálculo de costo total
   - Confirmar que los items existen en el sistema

2. **Validar cantidades en BOM**
   - Asegurar que ninguna cantidad sea 0
   - Confirmar que la lista de materiales no se cree sin items

3. **Generar Work Order**
   - Crear WO desde un BOM válido
   - Verificar estados iniciales y dependencias

4. **Actualizar Work Order**
   - Cambiar cantidad
   - Cambiar estado a "In Process" y "Completed"
   - Validar la coherencia del workflow

5. **Planificación de producción**
   - Simular programación de producción
   - Verificar asignación de estaciones de trabajo
   - Validar tiempos y rutas

## Prompt Ejemplo para IA
"Genera un plan detallado de pruebas E2E para el módulo Manufacturing en ERPNext. Incluye escenarios para BOM, Work Orders, cálculo de costos, validaciones de cantidad y planificación de producción con estaciones de trabajo."

## Integración con Gemini y Groq
- Usa `GOOGLE_GEMINI_API_KEY` para Google Gemini.
- Usa `GROQ_API_KEY` para consultas Groq.
- Construye prompts de texto con los casos de prueba arriba.
- Convierte las respuestas en scripts de pruebas o en prompts estructurados para generación automática.

## Archivos de referencia
- `tests/e2e/test_manufacturing_e2e.py`
- `tests/e2e/README.md`
