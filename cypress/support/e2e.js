// Cypress support file for E2E tests
// This file runs before all tests

// Disable uncaught exception handling to continue tests on errors
Cypress.on('uncaught:exception', (err, runnable) => {
  // Return false to prevent Cypress from failing the test
  return false;
});

// Handle network errors gracefully
beforeEach(() => {
  cy.on('fail', (error) => {
    if (error.message.includes('ECONNREFUSED') || error.message.includes('ERR_FAILED')) {
      cy.log('Network error detected. Continuing test...');
      throw error;
    }
  });
});
