import 'dotenv/config';
import { z } from 'zod';
import { createGroqStagehand } from './src/stagehand-groq.ts';

async function main(): Promise<void> {
  const stagehand = createGroqStagehand();

  try {
    await stagehand.init();
    const page = stagehand.page;

    console.log('=== GROQ - MANUFACTURING TEST ===');
    console.log('Abriendo página de demostración...');
    await page.goto('https://the-internet.herokuapp.com/');

    console.log('Búsqueda de flujo de Manufacturing/BOM en la página...');
    const observations = await page.observe(
      'Encuentra y describe la sección o enlace más parecido a un flujo de Manufacturing, BOM o producción.'
    );
    console.log('Observaciones de la IA:');
    console.log(observations);

    console.log('Extrayendo datos estructurados para Manufacturing...');
    const result = await page.extract({
      instruction:
        'Extrae el título principal de la página, el texto del enlace más relevante a producción y un breve ejemplo de cómo esto se relacionaría con el módulo Manufacturing.',
      schema: z.object({
        title: z.string(),
        relevant_link: z.string(),
        manufacturing_example: z.string(),
      }),
    });

    console.log('Resultado estructurado:');
    console.log(JSON.stringify(result, null, 2));

    console.log('Prueba Manufacturing con Groq finalizada.');
  } finally {
    await stagehand.close();
  }
}

main().catch((error) => {
  console.error('La prueba falló:', error);
  process.exit(1);
});
