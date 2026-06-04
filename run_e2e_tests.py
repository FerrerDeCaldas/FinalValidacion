#!/usr/bin/env python
"""
Quick Start Guide for E2E Tests
Examples of how to run the tests
"""

import subprocess
import sys


def run_all_tests():
    """Run all E2E tests"""
    print("Running all E2E tests...")
    cmd = [sys.executable, "-m", "pytest", "tests/e2e/", "-v"]
    subprocess.run(cmd)


def run_manufacturing_tests():
    """Run Manufacturing module tests"""
    print("Running Manufacturing E2E tests...")
    cmd = [sys.executable, "-m", "pytest", "tests/e2e/test_manufacturing_e2e.py", "-v"]
    subprocess.run(cmd)


def run_quality_tests():
    """Run Quality Management module tests"""
    print("Running Quality Management E2E tests...")
    cmd = [sys.executable, "-m", "pytest", "tests/e2e/test_quality_management_e2e.py", "-v"]
    subprocess.run(cmd)


def run_shopping_cart_tests():
    """Run Shopping Cart module tests"""
    print("Running Shopping Cart E2E tests...")
    cmd = [sys.executable, "-m", "pytest", "tests/e2e/test_shopping_cart_e2e.py", "-v"]
    subprocess.run(cmd)


def run_specific_test(test_name):
    """Run a specific test"""
    print(f"Running test: {test_name}...")
    cmd = [sys.executable, "-m", "pytest", "-k", test_name, "-v"]
    subprocess.run(cmd)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "all":
            run_all_tests()
        elif command == "manufacturing":
            run_manufacturing_tests()
        elif command == "quality":
            run_quality_tests()
        elif command == "shopping":
            run_shopping_cart_tests()
        elif command.startswith("test_"):
            run_specific_test(command)
        else:
            print(f"Unknown command: {command}")
            print("\nUsage:")
            print("  python run_e2e_tests.py all              - Run all tests")
            print("  python run_e2e_tests.py manufacturing   - Run manufacturing tests")
            print("  python run_e2e_tests.py quality         - Run quality management tests")
            print("  python run_e2e_tests.py shopping        - Run shopping cart tests")
            print("  python run_e2e_tests.py test_<name>     - Run specific test")
    else:
        print("E2E Tests Runner")
        print("================\n")
        print("Usage:")
        print("  python run_e2e_tests.py all              - Run all tests")
        print("  python run_e2e_tests.py manufacturing   - Run manufacturing tests")
        print("  python run_e2e_tests.py quality         - Run quality management tests")
        print("  python run_e2e_tests.py shopping        - Run shopping cart tests")
        print("  python run_e2e_tests.py test_<name>     - Run specific test")
        print("\nOr use pytest directly:")
        print("  pytest tests/e2e/ -v")
        print("  pytest tests/e2e/test_manufacturing_e2e.py -v")
        print("  pytest tests/e2e/ -k 'bom' -v")
