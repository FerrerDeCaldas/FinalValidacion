import { Stagehand } from "@browserbasehq/stagehand";

export function createGroqStagehand() {
  const apiKey = process.env.GROQ_API_KEY;
  if (!apiKey) {
    throw new Error("Falta la variable de entorno GROQ_API_KEY");
  }

  return new Stagehand({
    env: "LOCAL",
    model: process.env.GROQ_MODEL || "groq-1.0",
    modelClientOptions: {
      apiKey,
      baseURL: process.env.GROQ_BASE_URL || "https://api.groq.com",
    },
    localBrowserLaunchOptions: {
      headless: process.env.HEADLESS !== "false",
    },
  });
}
