#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Unit Tests Runner for Manufacturing, Quality Management, and Shopping Cart modules

This script demonstrates how to run the unit tests with various configurations.
Run this script from the project root directory.

Usage:
    python run_tests.py                    # Run all tests
    python run_tests.py manufacturing      # Run manufacturing tests only
    python run_tests.py quality            # Run quality management tests only
    python run_tests.py shopping_cart      # Run shopping cart tests only
    python run_tests.py --coverage         # Run with coverage report
"""

import subprocess
import sys
from pathlib import Path


def run_all_tests():
    """Run all unit tests"""
    print("=" * 70)
    print("Running ALL Unit Tests")
    print("=" * 70)
    subprocess.run(
        [sys.executable, "-m", "pytest", "tests/unit/", "-v", "--tb=short"],
        cwd=Path(__file__).parent
    )


def run_manufacturing_tests():
    """Run manufacturing module tests only"""
    print("=" * 70)
    print("Running Manufacturing Module Tests")
    print("=" * 70)
    subprocess.run(
        [sys.executable, "-m", "pytest", "tests/unit/manufacturing/", "-v", "--tb=short"],
        cwd=Path(__file__).parent
    )


def run_quality_management_tests():
    """Run quality management module tests only"""
    print("=" * 70)
    print("Running Quality Management Module Tests")
    print("=" * 70)
    subprocess.run(
        [sys.executable, "-m", "pytest", "tests/unit/quality_management/", "-v", "--tb=short"],
        cwd=Path(__file__).parent
    )


def run_shopping_cart_tests():
    """Run shopping cart module tests only"""
    print("=" * 70)
    print("Running Shopping Cart Module Tests")
    print("=" * 70)
    subprocess.run(
        [sys.executable, "-m", "pytest", "tests/unit/shopping_cart/", "-v", "--tb=short"],
        cwd=Path(__file__).parent
    )


def run_with_coverage():
    """Run all tests with coverage report"""
    print("=" * 70)
    print("Running Tests with Coverage Report")
    print("=" * 70)
    subprocess.run(
        [
            sys.executable, "-m", "pytest", "tests/unit/",
            "--cov=erpnext.manufacturing",
            "--cov=erpnext.quality_management",
            "--cov=erpnext.shopping_cart",
            "--cov-report=html",
            "--cov-report=term-missing",
            "-v"
        ],
        cwd=Path(__file__).parent
    )


def main():
    """Main entry point"""
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        
        if arg == "manufacturing":
            run_manufacturing_tests()
        elif arg == "quality" or arg == "quality_management":
            run_quality_management_tests()
        elif arg == "shopping_cart":
            run_shopping_cart_tests()
        elif arg == "--coverage" or arg == "coverage":
            run_with_coverage()
        elif arg == "--help" or arg == "-h":
            print(__doc__)
        else:
            print(f"Unknown argument: {arg}")
            print(__doc__)
            sys.exit(1)
    else:
        run_all_tests()


if __name__ == "__main__":
    main()
