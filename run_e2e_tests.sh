#!/usr/bin/env bash
# Quick Start Script for E2E Tests

echo "============================================"
echo "E2E Tests Quick Start"
echo "============================================"
echo ""

# Check if pytest is installed
if ! command -v pytest &> /dev/null; then
    echo "❌ pytest not found. Installing..."
    pip install pytest pytest-frappe
fi

echo "✅ Environment ready"
echo ""
echo "Choose option:"
echo "1) Run all tests"
echo "2) Run Manufacturing tests"
echo "3) Run Quality Management tests"
echo "4) Run Shopping Cart tests"
echo "5) Run specific test"
echo ""
read -p "Enter option (1-5): " choice

case $choice in
    1)
        echo "Running all E2E tests..."
        pytest tests/e2e/ -v
        ;;
    2)
        echo "Running Manufacturing E2E tests..."
        pytest tests/e2e/test_manufacturing_e2e.py -v
        ;;
    3)
        echo "Running Quality Management E2E tests..."
        pytest tests/e2e/test_quality_management_e2e.py -v
        ;;
    4)
        echo "Running Shopping Cart E2E tests..."
        pytest tests/e2e/test_shopping_cart_e2e.py -v
        ;;
    5)
        read -p "Enter test name (e.g., test_create_bom): " test_name
        pytest tests/e2e/ -k "$test_name" -v
        ;;
    *)
        echo "Invalid option"
        ;;
esac
