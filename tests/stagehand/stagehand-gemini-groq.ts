/// <reference types="node" />

import dotenv from "dotenv";
import { Stagehand } from "@browserbasehq/stagehand";

declare const process: any;

dotenv.config();

type ModuleKey = "manufacturing" | "quality_management" | "shopping_cart" | "all";

interface StagehandTestCase {
  id: string;
  title: string;
  objective: string;
}

interface ModulePlan {
  name: string;
  description: string;
  tests: StagehandTestCase[];
  examplePrompt: string;
}

const MODULE_PLANS: Record<Exclude<ModuleKey, "all">, ModulePlan> = {
  manufacturing: {
    name: "Manufacturing",
    description:
      "Pruebas de Manufacturing sobre BOM, Work Orders, Production Planning y estaciones de trabajo.",
    tests: [
      {
        id: "MFG-01",
        title: "Crear BOM exitosamente",
        objective:
          "Validar la creación y cálculo de costos de una lista de materiales",
      },
      {
        id: "MFG-02",
        title: "Validar cantidades en BOM",
        objective:
          "Asegurar que las cantidades no sean 0 y que el BOM tenga al menos un item",
      },
      {
        id: "MFG-03",
        title: "Generar Work Order",
        objective:
          "Crear una orden de trabajo a partir de un BOM y validar su estado",
      },
      {
        id: "MFG-04",
        title: "Validar actualización de Work Order",
        objective: "Actualizar cantidad y estado de una orden de trabajo",
      },
      {
        id: "MFG-05",
        title: "Planificación de producción",
        objective:
          "Simular el planificador de producción y validar el uso de estaciones de trabajo",
      },
    ],
    examplePrompt:
      "Genera un plan de pruebas E2E para una lista de materiales y órdenes de trabajo en el módulo Manufacturing de ERPNext. Incluye validaciones de cantidad, costos y workflow de producción.",
  },
  quality_management: {
    name: "Quality Management",
    description:
      "Pruebas de Quality Management sobre procedimientos, revisiones, acciones correctivas, metas y reuniones.",
    tests: [
      {
        id: "QM-01",
        title: "Crear procedimiento de calidad",
        objective: "Validar inicialización y estructura de un procedimiento de calidad",
      },
      {
        id: "QM-02",
        title: "Crear revisión de calidad",
        objective:
          "Asegurar que la revisión validada pueda asociarse a un procedimiento y su estado cambie correctamente",
      },
      {
        id: "QM-03",
        title: "Registrar acción correctiva",
        objective:
          "Crear una acción de calidad con resolución y verificar el estado",
      },
      {
        id: "QM-04",
        title: "Crear meta de calidad",
        objective:
          "Generar un objetivo de calidad con indicadores y actualizar su progreso",
      },
      {
        id: "QM-05",
        title: "Flujo completo de calidad",
        objective:
          "Crear procedimiento, revisión, acción y meta dentro de un workflow integrado",
      },
    ],
    examplePrompt:
      "Genera casos de prueba para Quality Management en ERPNext que cubran procedimientos, revisiones, acciones correctivas y metas de calidad.",
  },
  shopping_cart: {
    name: "Shopping Cart",
    description:
      "Pruebas de Shopping Cart sobre carrito, orden de venta, pagos, impuestos y descuentos.",
    tests: [
      {
        id: "SC-01",
        title: "Crear carrito y orden de venta",
        objective:
          "Agregar items al carrito y validar la creación de una sales order",
      },
      {
        id: "SC-02",
        title: "Calcular total del carrito",
        objective: "Validar subtotales, descuentos y total final",
      },
      {
        id: "SC-03",
        title: "Aplicar descuento",
        objective:
          "Aplicar descuento por porcentaje y validar el precio final",
      },
      {
        id: "SC-04",
        title: "Calcular impuestos automáticos",
        objective:
          "Verificar impuestos en la orden de venta según la configuración fiscal",
      },
      {
        id: "SC-05",
        title: "Procesar pago exitoso",
        objective:
          "Simular un flujo de pago y validar el estado de la orden",
      },
    ],
    examplePrompt:
      "Genera un conjunto de pruebas E2E para el Shopping Cart de ERPNext, incluyendo carrito, descuentos, impuestos y pagos.",
  },
};

const BASE_URL = process.env.GOOGLE_GEMINI_BASE_URL || "https://api.google.com/gemini";
const API_KEY = process.env.GOOGLE_GEMINI_API_KEY;
const GROQ_KEY = process.env.GROQ_API_KEY;
const HEADLESS = process.env.HEADLESS === "true";

function createGeminiStagehand(modelName: string = "gemini-1.5") {
  if (!API_KEY || !GROQ_KEY) {
    throw new Error(
      "Faltan variables de entorno. Define GOOGLE_GEMINI_API_KEY y GROQ_API_KEY en tu .env."
    );
  }

  return new Stagehand({
    env: "LOCAL",
    model: modelName,
    modelClientOptions: {
      apiKey: API_KEY,
      baseURL: BASE_URL,
    },
    localBrowserLaunchOptions: {
      headless: HEADLESS,
    },
  });
}

function buildStagehandPrompt(moduleKey: ModuleKey) {
  if (moduleKey === "all") {
    const allPlans = Object.values(MODULE_PLANS);
    const allDescriptions = allPlans
      .map((plan) => `- ${plan.name}: ${plan.description}`)
      .join("\n");
    const allTests = allPlans
      .flatMap((plan) =>
        plan.tests.map(
          (test) => `- ${test.id} (${plan.name}): ${test.title} \n  Objetivo: ${test.objective}`
        )
      )
      .join("\n");

    return `Genera un conjunto de pruebas E2E para los módulos Manufacturing, Quality Management y Shopping Cart de ERPNext.\n\nDescripción general:\n${allDescriptions}\n\nCasos de prueba propuestos:\n${allTests}\n\nRequisitos:\n- Genera la salida en formato JSON válido con campos {id, title, module, description, steps, expected_result}.\n- Incluye al menos 5 casos de prueba por módulo.\n- Mantén el contenido en español.\n`;
  }

  const plan = MODULE_PLANS[moduleKey];
  const tests = plan.tests.map(
    (test) => `- ${test.id}: ${test.title} \n  Objetivo: ${test.objective}`
  );

  return `Genera un conjunto de pruebas E2E para el módulo ${plan.name} en ERPNext.\n\nDescripción: ${plan.description}\n\nCasos de prueba:\n${tests.join("\n")}\n\nRequisitos:\n- Genera la salida en formato JSON válido con campos {id, title, description, steps, expected_result}.\n- Incluye al menos 5 casos de prueba.\n- Mantén el contenido en español.\n`;
}

function isKnownModule(value: ModuleKey): value is Exclude<ModuleKey, "all"> {
  return value !== "all";
}

async function main() {
  const moduleArg = (process.argv[2] as ModuleKey | undefined) || "all";
  const modelArg = process.argv[3] || "gemini-1.5";

  if (!isKnownModule(moduleArg) && moduleArg !== "all") {
    console.error(
      "Uso: ts-node stagehand-gemini-groq.ts <manufacturing|quality_management|shopping_cart|all> [model]"
    );
    process.exit(1);
  }

  const stagehand = createGeminiStagehand(modelArg);
  await stagehand.init();

  const prompt = buildStagehandPrompt(moduleArg);

  console.log("Prompt generado:\n", prompt);
  console.log("Ejecutando Stagehand para:", moduleArg, "\n");

  await stagehand.act(`Genera un paquete de pruebas E2E para ERPNext usando este prompt:\n\n${prompt}`);
  await stagehand.waitForNavigation();

  console.log("Stagehand terminado. Revisa la sesión de navegación para verificar la salida.");
}

main().catch((error) => {
  console.error("Error en Stagehand:", error);
  process.exit(1);
});
