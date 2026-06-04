# Stagehand - Shopping Cart

## Objetivo
Crear un plan de pruebas para el módulo `shopping_cart` de ERPNext, con foco en gestión del carrito, órdenes de venta, pagos, impuestos y descuentos.

## Alcance
- Agregar y remover items del carrito
- Calcular subtotales, descuentos y total final
- Generar sales orders desde el carrito
- Calcular impuestos automáticos
- Procesar pagos y verificar estados

## Casos de prueba
1. **Crear carrito y orden de venta**
   - Agregar items
   - Confirmar creación de Sales Order

2. **Calcular total del carrito**
   - Verificar subtotal y totales
   - Confirmar aplicación de impuestos y cargos

3. **Aplicar descuento**
   - Validar descuento porcentual y descuento fijo
   - Verificar total final después del descuento

4. **Calcular impuestos automáticos**
   - Aplicar reglas fiscales según ubicación
   - Validar la composición del impuesto en la orden

5. **Procesar pago exitoso**
   - Simular el flujo de pago completo
   - Validar el estado final de la orden

## Prompt Ejemplo para IA
"Genera un conjunto de pruebas E2E para el Shopping Cart de ERPNext. Incluye carrito, descuentos, impuestos, creación de órdenes de venta y flujo de pago."

## Integración con Gemini y Groq
- Usa prompts definidos con los casos de prueba.
- Aprovecha Groq para filtrar prompts futuros o estructuras de prueba.
- Mantén las claves en variables de entorno, no en el repositorio.

## Archivos de referencia
- `tests/e2e/test_shopping_cart_e2e.py`
- `tests/e2e/README.md`
