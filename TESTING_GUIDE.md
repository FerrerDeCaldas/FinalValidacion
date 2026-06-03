# Guía Rápida de Pruebas Unitarias

## Estructura de Pruebas Creadas

Se han creado pruebas unitarias completas para las 3 funcionalidades principales:

```
tests/unit/
├── manufacturing/           # Pruebas de Manufacturing
│   ├── test_bom.py         # Pruebas de Bill of Materials
│   ├── test_work_order.py  # Pruebas de Work Order
│   └── test_production_planning.py  # Pruebas de Production Planning
│
├── quality_management/      # Pruebas de Quality Management
│   ├── test_quality_procedure.py    # Pruebas de Quality Procedure
│   └── test_quality_management_advanced.py  # Pruebas avanzadas
│
└── shopping_cart/           # Pruebas de Shopping Cart
    ├── test_shopping_cart.py        # Pruebas básicas
    └── test_shopping_cart_advanced.py  # Pruebas avanzadas
```

## Instalación de Dependencias

```bash
pip install -r requirements-test.txt
```

## Comandos Principales

### 1. Ejecutar todas las pruebas
```bash
pytest
# o
python run_tests.py
```

### 2. Ejecutar pruebas por módulo

**Manufacturing:**
```bash
pytest tests/unit/manufacturing/ -v
python run_tests.py manufacturing
```

**Quality Management:**
```bash
pytest tests/unit/quality_management/ -v
python run_tests.py quality
```

**Shopping Cart:**
```bash
pytest tests/unit/shopping_cart/ -v
python run_tests.py shopping_cart
```

### 3. Ejecutar una prueba específica
```bash
# Prueba individual
pytest tests/unit/manufacturing/test_bom.py::TestBOMTree::test_bom_tree_initialization_leaf_node -v

# Todas las pruebas de una clase
pytest tests/unit/manufacturing/test_bom.py::TestBOMTree -v

# Todas las pruebas de un archivo
pytest tests/unit/manufacturing/test_bom.py -v
```

### 4. Ejecutar con reporte de cobertura
```bash
pytest --cov=erpnext.manufacturing --cov=erpnext.quality_management --cov=erpnext.shopping_cart --cov-report=html
python run_tests.py --coverage
```

### 5. Opciones útiles
```bash
# Salida concisa
pytest -q

# Mostrar prints
pytest -s

# Parar en primer error
pytest -x

# Parar después de N fallos
pytest --maxfail=2

# Ejecutar solo pruebas fallidas
pytest --lf

# Mostrar los tests más lentos
pytest --durations=10

# Ejecución en paralelo (requiere pytest-xdist)
pytest -n auto
```

## Características de las Pruebas

### ✅ Patrón AAA (Arrange-Act-Assert)
Todas las pruebas siguen este patrón para mayor claridad:

```python
def test_example(self):
    # Arrange - Preparar datos
    item_code = "ITEM-001"
    qty = 5.0
    
    # Act - Ejecutar la acción
    result = calculate_total(item_code, qty)
    
    # Assert - Verificar resultado
    assert_that(result).is_equal_to(expected_value)
```

### ✅ Fluent Assertions
Uso de `assertpy` para assertions más legibles:

```python
# En lugar de
assert result == expected

# Usamos
assert_that(result).is_equal_to(expected).is_instance_of(float)

# Ejemplos
assert_that([1, 2, 3]).contains(2).does_not_contain(5)
assert_that(value).is_between(0, 100)
assert_that(dict_obj).contains_key('name', 'email')
```

### ✅ Mocks y Patches
Uso de `unittest.mock` para aislar unidades:

```python
@patch('erpnext.manufacturing.doctype.bom.bom.frappe')
def test_something(self, mock_frappe):
    mock_frappe.db.get_value = MagicMock(return_value=None)
    # Test code here
```

## Resumen de Pruebas por Módulo

### Manufacturing (43 pruebas)
- **test_bom.py:** 10 pruebas
  - Inicialización del árbol BOM
  - Validación de recursión
  - Estructura de datos
  
- **test_work_order.py:** 16 pruebas
  - Excepciones personalizadas
  - Validación de cantidades
  - Imports y estructura
  
- **test_production_planning.py:** 17 pruebas
  - Planificación de producción
  - Gestión de tarjetas de trabajo
  - Capacidad de estaciones de trabajo
  - Operaciones de enrutamiento

### Quality Management (41 pruebas)
- **test_quality_procedure.py:** 18 pruebas
  - Inicialización
  - Hooks del documento
  - Validación
  - Funcionalidad NestedSet
  
- **test_quality_management_advanced.py:** 23 pruebas
  - Flujos de trabajo de revisión
  - Gestión de no conformidades
  - Seguimiento de acciones
  - Metas de calidad
  - Reuniones de calidad

### Shopping Cart (57 pruebas)
- **test_shopping_cart.py:** 19 pruebas
  - Gestión de items
  - Validación
  - Cálculos de totales
  - Estructura del carrito
  
- **test_shopping_cart_advanced.py:** 38 pruebas
  - Cálculo de precios
  - Cálculo de impuestos
  - Procesamiento de pagos
  - Gestión de inventario
  - Operaciones de envío
  - Gestión de vales/cupones
  - Creación de órdenes

**Total: 141 Pruebas Unitarias**

## Salida Esperada

Cuando ejecutas las pruebas, deberías ver algo así:

```
============================= test session starts ==============================
platform win32 -- Python 3.11.0, pytest-7.0.0, py-1.11.0, pluggy-1.0.0
cachedir: .pytest_cache
rootdir: c:\Users\User\Desktop\FinalValidacion, configfile: pytest.ini
collected 141 items

tests/unit/manufacturing/test_bom.py ............ [ 10%]
tests/unit/manufacturing/test_work_order.py ................ [ 21%]
tests/unit/manufacturing/test_production_planning.py ................. [ 32%]
tests/unit/quality_management/test_quality_procedure.py .................. [ 45%]
tests/unit/quality_management/test_quality_management_advanced.py ........................... [ 61%]
tests/unit/shopping_cart/test_shopping_cart.py ........................... [ 75%]
tests/unit/shopping_cart/test_shopping_cart_advanced.py ................................ [ 100%]

============================== 141 passed in 0.15s ===============================
```

## Solución de Problemas

### ImportError: No module named 'pytest'
```bash
pip install pytest
```

### ImportError: No module named 'assertpy'
```bash
pip install assertpy
```

### Tests no se encuentran
Asegúrate de estar en el directorio raíz del proyecto:
```bash
cd c:\Users\User\Desktop\FinalValidacion
pytest
```

### No se pueden importar módulos de erpnext
Asegúrate de que el directorio del proyecto está en PYTHONPATH:
```bash
set PYTHONPATH=%cd%;%PYTHONPATH%
pytest
```

## Buenas Prácticas

1. **Mantén las pruebas rápidas**: Las pruebas deben ejecutarse en milisegundos
2. **Una aserta por prueba**: Preferiblemente una afirmación por prueba
3. **Nombres descriptivos**: `test_should_calculate_correct_total_with_discount`
4. **Fixtures reutilizables**: Define fixtures en `conftest.py`
5. **Mocks para dependencias**: Usa mocks para aislar la unidad bajo prueba
6. **Pruebas independientes**: No dependa de orden de ejecución

## Más Información

Ver [tests/unit/README.md](tests/unit/README.md) para documentación completa.
