@echo off
REM Cypress E2E Test Runner Script for Windows

setlocal enabledelayedexpansion

echo ================================
echo Cypress E2E Test Runner
echo ================================
echo.

REM Check if a base URL is provided as argument
if "%1"=="" (
    set BASE_URL=http://localhost:8000
) else (
    set BASE_URL=%1
)

echo Base URL: !BASE_URL!
echo.

REM Set environment variable
set CYPRESS_BASE_URL=!BASE_URL!

echo Choose test mode:
echo 1) Run all E2E tests (headless)
echo 2) Run Performance tests (headless)
echo 3) Run Regression tests (headless)
echo 4) Run Security tests (headless)
echo 5) Run all modules test
echo.
set /p choice="Enter your choice (1-5): "

if "%choice%"=="1" (
    echo Running E2E tests...
    npx cypress run --spec tests/e2e/cypress-module-e2e.spec.ts
) else if "%choice%"=="2" (
    echo Running Performance tests...
    npx cypress run --spec tests/performance-testing/cypress-module-performance.spec.ts
) else if "%choice%"=="3" (
    echo Running Regression tests...
    npx cypress run --spec tests/regression-testing/cypress-module-regression.spec.ts
) else if "%choice%"=="4" (
    echo Running Security tests...
    npx cypress run --spec tests/security-testing/cypress-module-security.spec.ts
) else if "%choice%"=="5" (
    echo Running all module tests...
    npx cypress run --spec "tests/**/*-module-*.spec.ts"
) else (
    echo Invalid choice
    exit /b 1
)

endlocal
