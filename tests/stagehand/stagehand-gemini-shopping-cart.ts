import 'dotenv/config';
import { z } from 'zod';
import { createGeminiStagehand } from './src/stagehand-gemini.ts';

async function main(): Promise<void> {
  const stagehand = createGeminiStagehand();

  try {
    await stagehand.init();
    const page = stagehand.page;

    console.log('=== GEMINI - SHOPPING CART TEST ===');
    console.log('Abriendo página de demostración...');
    await page.goto('https://the-internet.herokuapp.com/');

    console.log('Búsqueda de flujo de Shopping Cart en la página...');
    const observations = await page.observe(
      'Encuentra y describe la sección o enlace más parecido a un flujo de carrito de compras o carrito de ordenes.'
    );
    console.log('Observaciones de la IA:');
    console.log(observations);

    console.log('Extrayendo datos estructurados para Shopping Cart...');
    const result = await page.extract({
      instruction:
        'Extrae el título principal de la página, el texto del enlace más relevante a carrito de compras y un ejemplo de cómo encajaría esto en un Shopping Cart.',
      schema: z.object({
        title: z.string(),
        relevant_link: z.string(),
        shopping_cart_example: z.string(),
      }),
    });

    console.log('Resultado estructurado:');
    console.log(JSON.stringify(result, null, 2));

    console.log('Prueba Shopping Cart con Gemini finalizada.');
  } finally {
    await stagehand.close();
  }
}

main().catch((error) => {
  console.error('La prueba falló:', error);
  process.exit(1);
});
