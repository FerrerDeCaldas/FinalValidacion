import 'dotenv/config';
import { z } from 'zod';
import { createGeminiStagehand } from './src/stagehand-gemini.ts';

async function main(): Promise<void> {
  const stagehand = createGeminiStagehand();

  try {
    await stagehand.init();
    const page = stagehand.page;

    console.log('=== GEMINI - QUALITY MANAGEMENT TEST ===');
    console.log('Abriendo página de demostración...');
    await page.goto('https://the-internet.herokuapp.com/');

    console.log('Búsqueda de flujo de Quality Management en la página...');
    const observations = await page.observe(
      'Encuentra y describe la sección o enlace más parecido a un flujo de Quality Management, revisión o control de calidad.'
    );
    console.log('Observaciones de la IA:');
    console.log(observations);

    console.log('Extrayendo datos estructurados para Quality Management...');
    const result = await page.extract({
      instruction:
        'Extrae el título principal de la página, el texto del enlace más relevante a control de calidad y una explicación breve de cómo se relaciona con Quality Management.',
      schema: z.object({
        title: z.string(),
        relevant_link: z.string(),
        quality_management_example: z.string(),
      }),
    });

    console.log('Resultado estructurado:');
    console.log(JSON.stringify(result, null, 2));

    console.log('Prueba Quality Management con Gemini finalizada.');
  } finally {
    await stagehand.close();
  }
}

main().catch((error) => {
  console.error('La prueba falló:', error);
  process.exit(1);
});
