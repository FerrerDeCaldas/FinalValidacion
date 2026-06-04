# Stagehand - Quality Management

## Objetivo
Crear un plan de pruebas para el módulo `quality_management` de ERPNext, con foco en procedimientos, revisiones, acciones correctivas, metas y reuniones.

## Alcance
- Crear procedimientos de calidad
- Registrar revisiones con objetivos
- Crear acciones correctivas y validarlas
- Definir metas de calidad y objetivos asociados
- Documentar reuniones y feedback

## Casos de prueba
1. **Crear procedimiento de calidad**
   - Validar estructura de procedimiento
   - Confirmar que el procedimiento permite pasos jerárquicos

2. **Crear revisión de calidad**
   - Asociar revisión a un procedimiento
   - Cambiar estado y verificar validaciones

3. **Registrar acción correctiva**
   - Crear acción con descripción y resolución
   - Verificar cambio de estado

4. **Crear meta de calidad**
   - Asegurar que las metas acepten objetivos y plazos
   - Actualizar el progreso y validar los indicadores

5. **Flujo completo de Quality Management**
   - Crear procedimiento, revisión, acción y meta en un workflow integrado
   - Validar la conexión de todos los objetos

## Prompt Ejemplo para IA
"Genera casos de prueba E2E para Quality Management en ERPNext que cubran procedimientos de calidad, revisiones, acciones correctivas, metas y reuniones. Incluye validaciones de estados y flujo de datos entre documentos."

## Integración con Gemini y Groq
- Usa tus claves de entorno para generar prompts seguros.
- Convierte los casos de prueba en instrucciones estructuradas para un modelo de texto.
- Aplica Groq si necesitas filtrar o buscar ejemplos de datos en un repositorio de prompts.

## Archivos de referencia
- `tests/e2e/test_quality_management_e2e.py`
- `tests/e2e/README.md`
