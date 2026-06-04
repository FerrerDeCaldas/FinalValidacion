# Stagehand Groq

## Descripción
Este archivo contiene el flujo de pruebas Stagehand para Groq.

## Archivos
- `stagehand-groq.ts`: script principal que ejecuta la prueba.
- `src/stagehand-groq.ts`: fábrica de Stagehand configurada para Groq.

## Flujo
1. Inicia Stagehand con `createGroqStagehand()`.
2. Abre `https://the-internet.herokuapp.com/`.
3. Observa el enlace de login.
4. Extrae el título principal y hasta cinco ejemplos.
5. Devuelve el resultado estructurado en JSON.

## Ejecución
```powershell
cd tests\stagehand
npm install
npx ts-node stagehand-groq.ts
```
