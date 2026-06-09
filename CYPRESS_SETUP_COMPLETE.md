# Setup Cypress - Resumen Completado ✅

## Lo que se ha realizado

### 1. **Creación de Pruebas Cypress**
Se han creado 4 archivos de prueba con casos para las 3 funcionalidades solicitadas:

```
tests/e2e/cypress-module-e2e.spec.ts                    ✅ Pruebas E2E
tests/performance-testing/cypress-module-performance.spec.ts ✅ Pruebas de Rendimiento
tests/regression-testing/cypress-module-regression.spec.ts   ✅ Pruebas de Regresión
tests/security-testing/cypress-module-security.spec.ts       ✅ Pruebas de Seguridad
```

**Módulos cubiertos:**
- ✅ Quality Management / Gestión de Calidad
- ✅ Shopping Cart / Carrito de Compras
- ✅ Manufacturing / Producción

### 2. **Instalación de Cypress**
```bash
✅ npm install cypress --save-dev
✅ Cypress version: 15.17.0
```

### 3. **Configuración**

**Archivos creados:**
- `cypress.config.js` - Configuración principal
- `cypress.env.json` - Variables de ambiente
- `cypress/support/e2e.js` - Support file para setup global

**Scripts en package.json:**
```json
"cypress:open": "npx cypress open",
"cypress:run": "npx cypress run"
```

### 4. **Scripts Helper**
- `run-cypress-tests.bat` - Para Windows (menú interactivo)
- `run-cypress-tests.sh` - Para Linux/Mac (menú interactivo)

### 5. **Documentación**
- `CYPRESS_GUIDE.md` - Guía completa de uso

---

## Cómo Usar

### Opción 1: Scripts Helper (Recomendado)

**Windows:**
```powershell
.\run-cypress-tests.bat
```

**Linux/Mac:**
```bash
bash run-cypress-tests.sh
```

### Opción 2: npm scripts

```bash
# Correr pruebas en modo headless
npm run cypress:run

# Abrir interfaz interactiva
npm run cypress:open
```

### Opción 3: npx directo

```bash
# Pruebas E2E
npx cypress run --spec tests/e2e/cypress-module-e2e.spec.ts

# Pruebas de Rendimiento
npx cypress run --spec tests/performance-testing/cypress-module-performance.spec.ts

# Pruebas de Regresión
npx cypress run --spec tests/regression-testing/cypress-module-regression.spec.ts

# Pruebas de Seguridad
npx cypress run --spec tests/security-testing/cypress-module-security.spec.ts

# Todas las pruebas
npx cypress run --spec "tests/**/*-module-*.spec.ts"
```

---

## Prerequisitos para ejecutar las pruebas

⚠️ **Importante:** Para ejecutar las pruebas, necesitas:

1. **ERPNext corriendo** en `http://localhost:8000` (o configura `CYPRESS_BASE_URL`)
2. **Credenciales válidas** en `cypress.env.json`
3. **Datos de prueba** (items, clientes, etc.) en tu instancia ERPNext

### Configurar Variables de Ambiente

**Opción A: Archivo `cypress.env.json`**
```json
{
  "ERP_USER": "tu-usuario@example.com",
  "ERP_PASSWORD": "tu-contraseña",
  "ERP_TOKEN": "tu-token-api"
}
```

**Opción B: Variable de ambiente**
```bash
set CYPRESS_BASE_URL=http://tu-servidor-erpnext.com:8000
```

---

## Estructura de Pruebas

### 📋 E2E Tests (`cypress-module-e2e.spec.ts`)
- Crear procedimiento de calidad
- Agregar producto al carrito
- Crear BOM y orden de trabajo

### ⚡ Performance Tests (`cypress-module-performance.spec.ts`)
- Medir tiempo de carga (<500ms)
- Validar respuesta del servidor

### 🔄 Regression Tests (`cypress-module-regression.spec.ts`)
- Validar campos requeridos
- Verificar cálculos
- Probar manejo de errores

### 🔒 Security Tests (`cypress-module-security.spec.ts`)
- Requerir autenticación
- Validar tokens
- Prevenir inyección SQL

---

## Archivos Generados

```
FinalValidacion/
├── cypress.config.js                    ← Configuración principal
├── cypress.env.json                     ← Variables de ambiente
├── run-cypress-tests.bat               ← Script para Windows
├── run-cypress-tests.sh                ← Script para Linux/Mac
├── CYPRESS_GUIDE.md                    ← Guía detallada
├── cypress/
│   └── support/
│       └── e2e.js                      ← Global setup
├── tests/
│   ├── e2e/
│   │   └── cypress-module-e2e.spec.ts
│   ├── performance-testing/
│   │   └── cypress-module-performance.spec.ts
│   ├── regression-testing/
│   │   └── cypress-module-regression.spec.ts
│   └── security-testing/
│       └── cypress-module-security.spec.ts
```

---

## Solución de Problemas

### ❌ "Cypress open" falla con ERR_FAILED

**Causa:** Problema conocido en Windows con el Launchpad de Cypress.

**Solución:** Usa modo headless
```bash
npx cypress run --spec tests/e2e/cypress-module-e2e.spec.ts
```

### ❌ "Failed to connect to baseUrl"

**Causa:** ERPNext no está corriendo o URL incorrecta.

**Solución:**
1. Inicia ERPNext en el puerto configurado
2. Verifica la URL en `cypress.env.json`
3. Prueba accediendo a la URL en el navegador

### ❌ "Cannot find module"

**Solución:**
```bash
npm install --ignore-scripts
```

---

## Versiones

- **Cypress:** 15.17.0
- **Node:** 22.19.0
- **Electron:** 37.6.0

---

## Próximos pasos

1. ✅ Instancia de ERPNext corriendo
2. ✅ Configurar `cypress.env.json` con credenciales
3. ✅ Crear datos de prueba en ERPNext
4. ✅ Ejecutar pruebas con `npm run cypress:run`
5. ✅ Ver reportes de ejecución

---

**¡Listo! Cypress está configurado y listo para usar.** 🎉
