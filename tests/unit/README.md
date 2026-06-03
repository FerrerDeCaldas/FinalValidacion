# Unit Tests

Pruebas unitarias para las 3 funcionalidades principales: Manufacturing, Quality Management y Shopping Cart.

## Estructura

```
tests/
├── conftest.py                 # Configuración compartida de pytest y fixtures
└── unit/
    ├── __init__.py
    ├── manufacturing/          # Pruebas del módulo Manufacturing
    │   ├── __init__.py
    │   ├── test_bom.py        # Pruebas para BOM (Bill of Materials)
    │   └── test_work_order.py # Pruebas para Work Order
    ├── quality_management/     # Pruebas del módulo Quality Management
    │   ├── __init__.py
    │   └── test_quality_procedure.py # Pruebas para Quality Procedures
    └── shopping_cart/          # Pruebas del módulo Shopping Cart
        ├── __init__.py
        └── test_shopping_cart.py    # Pruebas para Shopping Cart
```

## Características de las Pruebas

### 1. Patrón AAA (Arrange-Act-Assert)
Todas las pruebas siguen el patrón AAA:
- **Arrange**: Preparar datos y configuración
- **Act**: Ejecutar la lógica a probar
- **Assert**: Verificar resultados usando Fluent Assertions

### 2. Fluent Assertions
Se utiliza la librería `assertpy` para assertions fluidas y legibles:
```python
assert_that(result).is_equal_to(expected).is_instance_of(int)
assert_that(collection).is_not_empty().contains(item)
```

### 3. Mocks y Patches
Se utilizan `unittest.mock` para mockear dependencias externas:
```python
@patch('frappe')
def test_something(self, mock_frappe):
    mock_frappe.db.get_value = MagicMock(return_value=None)
```

## Instalación de Dependencias

```bash
pip install -r requirements-test.txt
```

## Ejecutar Pruebas

### Ejecutar todas las pruebas
```bash
pytest
```

### Ejecutar pruebas de un módulo específico
```bash
# Manufacturing
pytest tests/unit/manufacturing/

# Quality Management
pytest tests/unit/quality_management/

# Shopping Cart
pytest tests/unit/shopping_cart/
```

### Ejecutar una prueba específica
```bash
pytest tests/unit/manufacturing/test_bom.py::TestBOMTree::test_bom_tree_initialization_leaf_node
```

### Ejecutar con cobertura
```bash
pytest --cov=erpnext.manufacturing --cov=erpnext.quality_management --cov=erpnext.shopping_cart --cov-report=html
```

### Ver salida detallada
```bash
pytest -v
```

### Ejecutar solo pruebas rápidas
```bash
pytest -m "not slow"
```

## Estructura de Pruebas

### Manufacturing Module

#### test_bom.py
- **TestBOMTree**: Pruebas de la estructura del árbol de BOM
  - Inicialización de nodos hoja
  - Inicialización de items hijos
  - Cálculos de cantidades
  
- **TestBOMValidation**: Pruebas de validación
  - Errores de recursión circular
  - Manejo de excepciones
  
- **TestBOMDataStructure**: Pruebas de estructura de datos
  - Uso de `__slots__` para eficiencia de memoria
  - Accesibilidad de atributos

#### test_work_order.py
- **TestWorkOrderErrors**: Pruebas de excepciones personalizadas
  - OverProductionError
  - CapacityError
  - StockOverProductionError
  - OperationTooLongError
  - ItemHasVariantError
  - SerialNoQtyError
  
- **TestWorkOrderException**: Pruebas de lanzamiento de excepciones
  
- **TestWorkOrderImports**: Pruebas de importaciones correctas
  
- **TestWorkOrderQuantityValidation**: Pruebas de validación de cantidades

### Quality Management Module

#### test_quality_procedure.py
- **TestQualityProcedureInitialization**: Inicialización del documento
  - Campo NSM parent
  - Estructura de la clase
  
- **TestQualityProcedureHooks**: Pruebas de hooks del documento
  - before_save
  - on_update
  - after_insert
  - on_trash
  
- **TestQualityProcedureValidation**: Pruebas de validación
  - Validación de items hijos incorrectos
  - Validación de campos parent
  
- **TestQualityProcedureNestedSet**: Pruebas de funcionalidad NestedSet
  - Herencia de NestedSet
  - Campos específicos
  
- **TestQualityReviewValidation**: Pruebas de lógica de Quality Review
  - Estados válidos
  - Rangos de calificación
  - Validación de longitud de feedback

### Shopping Cart Module

#### test_shopping_cart.py
- **TestShoppingCartInitialization**: Inicialización del módulo
  
- **TestShoppingCartItemManagement**: Manejo de items
  - Cantidades positivas
  - Precios válidos
  - Cálculo de totales
  
- **TestShoppingCartValidation**: Reglas de validación
  - Incremento/decremento de cantidades
  - Validaciones de cantidad
  
- **TestShoppingCartTotals**: Lógica de cálculos
  - Subtotal
  - Descuentos
  - Impuestos
  - Total final
  
- **TestShoppingCartCart**: Estructura de datos del carrito
  - Carrito vacío
  - Agregar items
  - Remover items
  - Limpiar carrito

## Ejemplo de Prueba

```python
class TestBOMTree:
    """Test suite for BOM Tree structure and operations"""

    @patch('erpnext.manufacturing.doctype.bom.bom.frappe')
    def test_bom_tree_initialization_leaf_node(self, mock_frappe):
        # Arrange
        item_code = "ITEM-001"
        qty = 5.0
        exploded_qty = 10.0

        # Act
        from erpnext.manufacturing.doctype.bom.bom import BOMTree
        bom_tree = BOMTree(name=item_code, is_bom=False, qty=qty, exploded_qty=exploded_qty)

        # Assert
        assert_that(bom_tree).is_not_none()
        assert_that(bom_tree.name).is_equal_to(item_code)
        assert_that(bom_tree.qty).is_equal_to(qty)
```

## Notas

- Las pruebas utilizan mocks para aislar las unidades bajo prueba
- Se evita acceso a bases de datos reales
- Las pruebas son independientes y pueden ejecutarse en cualquier orden
- Las pruebas se ejecutan rápidamente sin dependencias externas
