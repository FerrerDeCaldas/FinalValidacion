# Stagehand Gemini

## Descripción
Este archivo contiene el flujo de pruebas Stagehand para Google Gemini.

## Archivos
- `stagehand-gemini.ts`: script principal que ejecuta la prueba.
- `src/stagehand-gemini.ts`: fábrica de Stagehand configurada para Gemini.

## Flujo
1. Inicia Stagehand con `createGeminiStagehand()`.
2. Abre `https://the-internet.herokuapp.com/`.
3. Observa el enlace de login.
4. Extrae el título principal y hasta cinco ejemplos.
5. Devuelve el resultado estructurado en JSON.

## Ejecución
```powershell
cd tests\stagehand
npm install
npx ts-node stagehand-gemini.ts
```
