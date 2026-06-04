# Stagehand - Todas las funcionalidades

## Objetivo
Generar un plan de pruebas Stagehand que cubra las tres funcionalidades principales de ERPNext:
- `manufacturing`
- `quality_management`
- `shopping_cart`

## Resumen
Este documento describe los casos de prueba de alto nivel para cada módulo y cómo un modelo de IA puede generar scripts de prueba automáticos.

## Módulos y cobertura

### 1. Manufacturing
- Pruebas de creación de BOM
- Validación de cantidades y estructura de la lista de materiales
- Cálculo de costos totales del BOM
- Creación y actualización de órdenes de trabajo
- Validación de la planificación de producción y asignación de estaciones de trabajo

### 2. Quality Management
- Creación de procedimientos de calidad
- Revisiones de calidad y objetivos asociados
- Acciones correctivas con estado y resoluciones
- Metas de calidad con indicadores y progreso
- Flujo integrado: procedimiento -> revisión -> acción -> meta

### 3. Shopping Cart
- Gestión de carrito y items
- Cálculo de totales con descuentos e impuestos
- Creación de Sales Order desde el carrito
- Procesamiento de pagos básicos
- Validación de actualizaciones, eliminación de items y cambios de cantidad

## Casos de prueba por módulo

### Manufacturing
- MFG-01: Crear BOM con múltiples items
- MFG-02: Validar cantidad y obligatoriedad de items en BOM
- MFG-03: Calcular costo total correcto en BOM
- MFG-04: Crear Work Order desde BOM
- MFG-05: Actualizar Work Order y verificar estado

### Quality Management
- QM-01: Crear procedimiento de calidad
- QM-02: Crear revisión de calidad
- QM-03: Registrar acción correctiva
- QM-04: Crear meta de calidad
- QM-05: Flujo completo de calidad integrado

### Shopping Cart
- SC-01: Crear carrito y Sales Order
- SC-02: Calcular total correcto del carrito
- SC-03: Aplicar descuento y validar total
- SC-04: Calcular impuestos automáticos en la orden
- SC-05: Procesar pago exitoso y validar estado

## Prompt para IA
"Genera un conjunto de pruebas E2E para los módulos Manufacturing, Quality Management y Shopping Cart de ERPNext. Cada caso debe incluir el identificador del módulo, el objetivo, los pasos clave y el resultado esperado. Devuelve la salida en JSON válido con campos {id, module, title, description, steps, expected_result}."

## Salida esperada
- JSON con al menos 5 casos de prueba por módulo
- Documentación clara para cada caso
- Enfoque en la estructura de prueba y la automatización

## Archivos de referencia
- `tests/e2e/test_manufacturing_e2e.py`
- `tests/e2e/test_quality_management_e2e.py`
- `tests/e2e/test_shopping_cart_e2e.py`
- `tests/stagehand/stagehand-gemini-groq.ts`
- `tests/stagehand/stagehand_plan.json`
