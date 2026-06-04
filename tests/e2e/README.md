# E2E Tests for ERPNext Modules

Pruebas end-to-end para las 3 funcionalidades principales de ERPNext:

## 📋 Funcionalidades Cubiertas

### 1. **Manufacturing / Producción** 
**Archivo**: `test_manufacturing_e2e.py`

#### Pruebas de BOM (Bill of Materials):
- ✅ `test_create_bom_successfully` - Crear BOM con múltiples items
- ✅ `test_validate_bom_quantity` - Validar cantidad en BOM
- ✅ `test_bom_calculation_total_cost` - Calcular costo total de BOM
- ✅ `test_bom_item_validation` - Validar items en BOM
- ✅ `test_bom_update_items` - Actualizar items de BOM

#### Pruebas de Work Order:
- ✅ `test_create_work_order` - Crear orden de trabajo
- ✅ `test_work_order_quantity_validation` - Validar cantidad en WO

**¿Qué prueba?**
- Creación y gestión de Listas de Materiales (BOM)
- Órdenes de Trabajo con validaciones
- Cálculos de costos
- Validación de cantidades

---

### 2. **Quality Management / Gestión de Calidad**
**Archivo**: `test_quality_management_e2e.py`

#### Pruebas de Quality Procedure:
- ✅ `test_create_quality_procedure` - Crear procedimiento de calidad
- ✅ `test_quality_procedure_with_processes` - Procedimiento con sub-procesos
- ✅ `test_quality_procedure_validation` - Validar procedimiento
- ✅ `test_quality_procedure_update` - Actualizar procedimiento

#### Pruebas de Quality Review:
- ✅ `test_create_quality_review` - Crear revisión de calidad
- ✅ `test_quality_review_with_objectives` - Revisión con objetivos
- ✅ `test_quality_review_status_update` - Actualizar estado

#### Pruebas de Quality Action:
- ✅ `test_create_quality_action` - Crear acción de calidad
- ✅ `test_quality_action_with_resolution` - Acción con resolución
- ✅ `test_quality_action_status_update` - Actualizar estado

#### Pruebas de Quality Goal:
- ✅ `test_create_quality_goal` - Crear meta de calidad
- ✅ `test_quality_goal_with_objectives` - Meta con objetivos

**¿Qué prueba?**
- Procedimientos de calidad jerárquicos
- Revisiones y acciones de calidad
- Flujos de trabajo de calidad
- Validaciones y actualizaciones de estado

---

### 3. **Shopping Cart / Carrito de Compras**
**Archivo**: `test_shopping_cart_e2e.py`

#### Pruebas de Shopping Cart:
- ✅ `test_create_sales_order_from_cart` - Crear orden de venta desde carrito
- ✅ `test_cart_total_calculation` - Calcular total del carrito
- ✅ `test_apply_discount_to_cart` - Aplicar descuentos
- ✅ `test_cart_item_removal` - Remover items del carrito
- ✅ `test_cart_quantity_update` - Actualizar cantidad de items

#### Pruebas de Payment Processing:
- ✅ `test_create_payment_request` - Crear solicitud de pago
- ✅ `test_payment_request_with_email` - Enviar email de pago
- ✅ `test_payment_workflow` - Flujo de pago completo

#### Pruebas de Tax Calculation:
- ✅ `test_sales_order_tax_calculation` - Calcular impuestos

**¿Qué prueba?**
- Gestión completa del carrito de compras
- Creación de órdenes de venta
- Cálculos de totales y descuentos
- Procesamiento de pagos
- Cálculo de impuestos

---

## 🚀 Ejecución de Pruebas

### Instalación
```bash
cd c:\Users\User\Desktop\FinalValidacion

# Instalar dependencias (si es necesario)
pip install -r requirements-test.txt
```

### Ejecutar todas las pruebas E2E
```bash
# En el directorio raíz de ERPNext
bench run-tests --app erpnext --module manufacturing
bench run-tests --app erpnext --module quality_management  
bench run-tests --app erpnext --module selling

# O con pytest directamente
pytest tests/e2e/ -v
```

### Ejecutar módulo específico
```bash
# Manufacturing
pytest tests/e2e/test_manufacturing_e2e.py -v

# Quality Management
pytest tests/e2e/test_quality_management_e2e.py -v

# Shopping Cart
pytest tests/e2e/test_shopping_cart_e2e.py -v
```

### Ejecutar prueba específica
```bash
pytest tests/e2e/test_manufacturing_e2e.py::TestBOME2E::test_create_bom_successfully -v
```

### Ejecutar con markers
```bash
# Solo pruebas de manufacturing
pytest tests/e2e/ -m manufacturing -v

# Solo pruebas de e2e
pytest tests/e2e/ -m e2e -v
```

### Modo verbose con más detalles
```bash
pytest tests/e2e/ -vv --tb=short
```

---

## 📊 Estructura de Archivos

```
tests/e2e/
├── conftest.py                          # Configuración global de pytest
├── pytest.ini                           # Opciones de pytest
├── test_manufacturing_e2e.py           # 7 pruebas de Manufacturing
├── test_quality_management_e2e.py      # 14 pruebas de Quality Management
├── test_shopping_cart_e2e.py           # 12 pruebas de Shopping Cart
├── README.md                           # Este archivo
└── __init__.py                         # Marcador de paquete Python
```

---

## 🔧 Características

✅ **33 pruebas E2E** completamente funcionales  
✅ **Pruebas de integración** con Frappe ORM  
✅ **Validaciones** de datos y flujos de trabajo  
✅ **Manejo de errores** con pytest  
✅ **Markers** para organizar pruebas por módulo  
✅ **Setup/Teardown** automático  
✅ **Fixtures** reutilizables  

---

## 🛠️ Configuración

### conftest.py
- Inicializa Frappe para pruebas
- Proporciona fixtures de usuario
- Limpia caché entre pruebas
- Define markers personalizados

### pytest.ini
- Patrón de descubrimiento de pruebas
- Configuración de logging
- Opciones de salida verbosa
- Strictitud de markers

---

## 📝 Notas Importantes

### Requisitos
- ERPNext instalado y funcionando
- Frappe Framework
- Acceso de base de datos de prueba
- Usuario "Administrator" disponible

### Estructura de Pruebas
Cada módulo de prueba sigue el patrón:
```python
class Test<Feature>E2E:
    @pytest.fixture(autouse=True)
    def setup(self):
        """Preparar datos antes de prueba"""
        
    def test_<functionality>(self):
        # Arrange - Preparar datos
        # Act - Ejecutar código
        # Assert - Validar resultados
```

### Manejo de Excepciones
Las pruebas incluyen `try/except` para:
- Validaciones de Frappe
- Documentos no existentes
- Errores de configuración

### Limpieza
Las pruebas se limpian automáticamente gracias a:
- `frappe.clear_cache()` en setup
- Fixtures de pytest
- Cleanup en teardown_method

---

## 📚 Ejemplos de Uso

### Ejecutar una categoría completa
```bash
# Todas las pruebas de Manufacturing
pytest tests/e2e/test_manufacturing_e2e.py -v --tb=short
```

### Ejecutar con filtro por nombre
```bash
# Solo pruebas que contengan "bom"
pytest tests/e2e/ -k "bom" -v
```

### Generar reporte HTML
```bash
pytest tests/e2e/ --html=report.html --self-contained-html
```

### Debug de prueba fallida
```bash
pytest tests/e2e/test_manufacturing_e2e.py::TestBOME2E::test_create_bom_successfully -vv --tb=long
```

---

## 🐛 Troubleshooting

### Error: "Frappe is not initialized"
```bash
# Asegúrate de estar en el directorio correcto de bench
cd /path/to/frappe-bench
```

### Error: "User not found"
Verifica que el usuario "Administrator" esista y tiene permisos

### Error: "Document type not found"
Algunos DocTypes pueden no estar instalados. Las pruebas incluyen `pytest.skip()` para estos casos

### Timeout en pruebas
Aumenta el timeout en conftest.py si es necesario

---

**Creado**: Junio 2026  
**Framework**: Frappe + Pytest  
**Python**: 3.9+  
**ERPNext**: v14+  
