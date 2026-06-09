const { defineConfig } = require('cypress');

module.exports = defineConfig({
  e2e: {
    specPattern: 'tests/**/*.spec.ts',
    // Use a baseUrl that won't fail verification, or make it configurable
    baseUrl: process.env.CYPRESS_BASE_URL,
    supportFile: 'cypress/support/e2e.js',
    defaultCommandTimeout: 10000,
    requestTimeout: 10000,
    responseTimeout: 10000,
    viewportWidth: 1280,
    viewportHeight: 720,
    video: false,
    screenshotOnRunFailure: false,
    numTestsKeptInMemory: 0,
    experimentalMemoryManagement: true,
    setupNodeEvents(on, config) {
      // Log when baseUrl is being used
      if (config.baseUrl) {
        console.log(`Using baseUrl: ${config.baseUrl}`);
      }

      const http = require('http');
      const https = require('https');

      on('task', {
        checkServer({ url }) {
          return new Promise((resolve) => {
            try {
              const lib = String(url).startsWith('https') ? https : http;
              const req = lib.request(url, { method: 'HEAD', timeout: 3000 }, (res) => {
                resolve({ status: res.statusCode });
              });
              req.on('error', (err) => resolve({ error: err.message }));
              req.on('timeout', () => {
                req.destroy();
                resolve({ error: 'timeout' });
              });
              req.end();
            } catch (e) {
              resolve({ error: e.message });
            }
          });
        },
      });

      return config;
    },
  },
  chromeWebSecurity: false,
  firefoxWebSecurity: false,
});
