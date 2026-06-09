#!/bin/bash
# Cypress E2E Test Runner Script for Linux/Mac

BASE_URL="${1:-http://localhost:8000}"

echo "================================"
echo "Cypress E2E Test Runner"
echo "================================"
echo ""
echo "Base URL: $BASE_URL"
echo ""
echo "Choose test mode:"
echo "1) Run all E2E tests (headless)"
echo "2) Run Performance tests (headless)"
echo "3) Run Regression tests (headless)"
echo "4) Run Security tests (headless)"
echo "5) Run all modules test"
echo ""
read -p "Enter your choice (1-5): " choice

export CYPRESS_BASE_URL="$BASE_URL"

case $choice in
    1)
        echo "Running E2E tests..."
        npx cypress run --spec tests/e2e/cypress-module-e2e.spec.ts
        ;;
    2)
        echo "Running Performance tests..."
        npx cypress run --spec tests/performance-testing/cypress-module-performance.spec.ts
        ;;
    3)
        echo "Running Regression tests..."
        npx cypress run --spec tests/regression-testing/cypress-module-regression.spec.ts
        ;;
    4)
        echo "Running Security tests..."
        npx cypress run --spec tests/security-testing/cypress-module-security.spec.ts
        ;;
    5)
        echo "Running all module tests..."
        npx cypress run --spec "tests/**/*-module-*.spec.ts"
        ;;
    *)
        echo "Invalid choice"
        exit 1
        ;;
esac
