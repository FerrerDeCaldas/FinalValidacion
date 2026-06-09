# Cypress E2E Tests - Setup and Usage Guide

## Overview

This project includes Cypress E2E tests for three key ERPNext modules:
- **Quality Management** (Gestión de Calidad)
- **Shopping Cart** (Carrito de Compras)  
- **Manufacturing** (Producción)

Tests are organized by category:
- `tests/e2e/` - End-to-End tests
- `tests/performance-testing/` - Performance benchmarks
- `tests/regression-testing/` - Regression test cases
- `tests/security-testing/` - Security validation tests

## Installation

Cypress is already installed as a dev dependency. To verify:

```bash
npm list cypress
# or
npx cypress --version
```

## Running Tests

### Option 1: Using npm scripts

```bash
# Run E2E tests in headless mode
npm run cypress:run

# Open Cypress interactive UI
npm run cypress:open
```

### Option 2: Using helper scripts

**Windows:**
```cmd
run-cypress-tests.bat
```

**Linux/Mac:**
```bash
bash run-cypress-tests.sh
```

### Option 3: Using npx directly

```bash
# Run specific test file
npx cypress run --spec tests/e2e/cypress-module-e2e.spec.ts

# Run all tests in a folder
npx cypress run --spec "tests/e2e/**/*.spec.ts"

# Run with specific browser
npx cypress run --browser firefox

# Run with verbose output
npx cypress run --spec tests/e2e/cypress-module-e2e.spec.ts --verbose
```

## Environment Variables

Set a custom base URL for tests:

```bash
# Windows
set CYPRESS_BASE_URL=http://your-erpnext-instance.com

# Linux/Mac
export CYPRESS_BASE_URL=http://your-erpnext-instance.com
```

Or configure in `cypress.env.json`:

```json
{
  "ERP_USER": "your-username@example.com",
  "ERP_PASSWORD": "your-password",
  "ERP_TOKEN": "your-api-token"
}
```

## Configuration

Cypress configuration is defined in `cypress.config.js`:

- **Base URL**: http://localhost:8000 (default)
- **Timeout**: 10 seconds per command
- **Viewport**: 1280x720
- **Video**: Disabled by default
- **Screenshots**: Only on failure

## Test Structure

### E2E Tests (`tests/e2e/cypress-module-e2e.spec.ts`)
- Create Quality Management procedures
- Add products to Shopping Cart
- Create Bills of Materials (BOM)
- Generate Work Orders

### Performance Tests (`tests/performance-testing/cypress-module-performance.spec.ts`)
- Measure page load times
- Verify performance benchmarks (<500ms)

### Regression Tests (`tests/regression-testing/cypress-module-regression.spec.ts`)
- Validate field requirements
- Test calculations and totals
- Verify error handling

### Security Tests (`tests/security-testing/cypress-module-security.spec.ts`)
- Test authentication requirements
- Validate token handling
- Check SQL injection prevention

## Prerequisites

Before running tests, ensure:

1. **ERPNext is running** at the configured base URL
2. **Valid credentials** are set in `cypress.env.json`
3. **Test data** (items, customers, etc.) exists in your ERPNext instance

## Troubleshooting

### Cypress open fails with "ERR_FAILED"

This is a known issue on Windows with Cypress Launchpad. Workaround:

```bash
# Use headless mode instead
npx cypress run --spec tests/e2e/cypress-module-e2e.spec.ts
```

### Tests fail with "Failed to connect to baseUrl"

Verify:
1. ERPNext is running on the configured base URL
2. Firewall allows connections to the ERPNext server
3. Base URL is correct in `cypress.env.json` or environment variable

### "Cannot find module" errors

Reinstall dependencies:

```bash
npm install --ignore-scripts
```

## Writing New Tests

Create a new test file in the appropriate folder:

```typescript
/// <reference types="cypress" />

describe('My New Test Suite', () => {
  beforeEach(() => {
    cy.visit('/app/dashboard');
  });

  it('should perform some action', () => {
    cy.contains('Expected Text').should('be.visible');
  });
});
```

For more information, see:
- [Cypress Documentation](https://docs.cypress.io)
- [ERPNext API Documentation](https://frappeframework.com/docs/user/en/api)

## CI/CD Integration

For automated testing in CI/CD pipelines:

```yaml
# Example GitHub Actions workflow
- name: Run Cypress tests
  run: |
    npm install --ignore-scripts
    npx cypress run --spec "tests/**/*.spec.ts"
  env:
    CYPRESS_BASE_URL: ${{ secrets.ERPNEXT_URL }}
```

## Support

For issues or questions about the tests, refer to:
- Test file comments
- Cypress documentation
- ERPNext module documentation
