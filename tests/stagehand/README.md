# Stagehand AI Test Plan

Esta carpeta contiene el scaffolding de Stagehand para los tres módulos solicitados:
- `manufacturing`
- `quality_management`
- `shopping_cart`

El objetivo es proporcionar un punto de partida con scripts TypeScript separados para Google Gemini y Groq.

> Nota importante: no se deben guardar claves o tokens directamente en el repositorio. Usa variables de entorno como `GEMINI_API_KEY` y `GROQ_API_KEY`.

## Requisitos

1. Node.js instalado.
2. Ejecutar `npm install` dentro de `tests/stagehand`.
3. Crear un archivo `.env` a partir de `.env.example`.

## Variables de entorno

Copia `.env.example` a `tests/stagehand/.env` y define tus claves:

```powershell
copy tests\stagehand\.env.example tests\stagehand\.env
```

Luego edita `tests/stagehand\.env` para asignar tus valores reales:

- `GEMINI_API_KEY`
- `GROQ_API_KEY`
- opcional: `GEMINI_MODEL`, `GROQ_MODEL`

## Instalación

```powershell
cd tests\stagehand
npm install
```

## Ejecución de los scripts

### Google Gemini

```powershell
cd tests\stagehand
npx ts-node stagehand-gemini.ts
```

### Gemini por módulo

```powershell
cd tests\stagehand
npx ts-node stagehand-gemini-manufacturing.ts
npx ts-node stagehand-gemini-quality-management.ts
npx ts-node stagehand-gemini-shopping-cart.ts
```

### Groq

```powershell
cd tests\stagehand
npx ts-node stagehand-groq.ts
```

### Groq por módulo

```powershell
cd tests\stagehand
npx ts-node stagehand-groq-manufacturing.ts
npx ts-node stagehand-groq-quality-management.ts
npx ts-node stagehand-groq-shopping-cart.ts
```

## Archivos principales

- `stagehand-gemini.ts` - flujo general Google Gemini
- `stagehand-gemini-manufacturing.ts` - Manufacturing con Gemini
- `stagehand-gemini-quality-management.ts` - Quality Management con Gemini
- `stagehand-gemini-shopping-cart.ts` - Shopping Cart con Gemini
- `stagehand-groq.ts` - flujo general Groq
- `stagehand-groq-manufacturing.ts` - Manufacturing con Groq
- `stagehand-groq-quality-management.ts` - Quality Management con Groq
- `stagehand-groq-shopping-cart.ts` - Shopping Cart con Groq
- `src/stagehand-gemini.ts` - fábrica Gemini
- `src/stagehand-groq.ts` - fábrica Groq

## Estado actual

- Los scripts compilan correctamente en TypeScript.
- La ejecución fallará si no se definen las variables de entorno `GEMINI_API_KEY` o `GROQ_API_KEY`.
- `stagehand-gemini.ts` y `stagehand-groq.ts` están listos para conectar con sus proveedores una vez que se configure la API.
