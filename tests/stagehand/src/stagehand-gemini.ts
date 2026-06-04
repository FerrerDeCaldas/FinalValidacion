import { Stagehand } from "@browserbasehq/stagehand";

export function createGeminiStagehand() {
  const apiKey = process.env.GEMINI_API_KEY;
  if (!apiKey) {
    throw new Error("Falta la variable de entorno GEMINI_API_KEY");
  }

  return new Stagehand({
    env: "LOCAL",
    model: process.env.GEMINI_MODEL || "gemini-1.5",
    modelClientOptions: {
      apiKey,
      baseURL: process.env.GEMINI_BASE_URL || "https://api.google.com/gemini",
    },
    localBrowserLaunchOptions: {
      headless: process.env.HEADLESS !== "false",
    },
  });
}
