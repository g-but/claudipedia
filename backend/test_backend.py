#!/usr/bin/env python3
"""
Test runner script for backend services.
"""

import subprocess
import sys
import os
from pathlib import Path


def run_tests():
    """Run all backend tests."""
    backend_dir = Path(__file__).parent
    os.chdir(backend_dir)

    print("🔍 Running backend tests...")

    # Check if pytest is available
    try:
        import pytest
    except ImportError:
        print("❌ pytest not found. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pytest", "pytest-asyncio"], check=True)

    # Run tests with verbose output and coverage
    result = subprocess.run([
        sys.executable, "-m", "pytest",
        "-v",
        "--cov=.",
        "--cov-report=html",
        "--cov-report=term",
        "--tb=short",
        "test_*.py"
    ], cwd=backend_dir)

    return result.returncode


def run_linting():
    """Run code linting and formatting checks."""
    backend_dir = Path(__file__).parent
    os.chdir(backend_dir)

    print("🔍 Running code quality checks...")

    # Install linting tools if not available
    try:
        import black
        import isort
        import flake8
    except ImportError:
        print("📦 Installing linting tools...")
        subprocess.run([
            sys.executable, "-m", "pip", "install",
            "black", "isort", "flake8"
        ], check=True)

    # Run black formatting check
    print("🎨 Checking code formatting (black)...")
    black_result = subprocess.run([
        sys.executable, "-m", "black", "--check", "."
    ], cwd=backend_dir)

    # Run import sorting check
    print("📋 Checking import sorting (isort)...")
    isort_result = subprocess.run([
        sys.executable, "-m", "isort", "--check-only", "."
    ], cwd=backend_dir)

    # Run flake8 linting
    print("🔍 Running linting (flake8)...")
    flake8_result = subprocess.run([
        sys.executable, "-m", "flake8", "."
    ], cwd=backend_dir)

    return black_result.returncode == 0 and isort_result.returncode == 0 and flake8_result.returncode == 0


def run_type_check():
    """Run type checking if mypy is available."""
    backend_dir = Path(__file__).parent
    os.chdir(backend_dir)

    print("🔍 Running type checking (mypy)...")

    try:
        import mypy
    except ImportError:
        print("⚠️  mypy not available, skipping type checking")
        return True

    # Run mypy type checking
    result = subprocess.run([
        sys.executable, "-m", "mypy", "."
    ], cwd=backend_dir)

    return result.returncode == 0


def main():
    """Main test runner function."""
    print("🚀 Starting Claudipedia Backend Test Suite")
    print("=" * 50)

    tests_passed = True

    # Run tests
    if run_tests() != 0:
        tests_passed = False
        print("❌ Tests failed!")

    # Run linting
    if not run_linting():
        tests_passed = False
        print("❌ Code quality checks failed!")

    # Run type checking
    if not run_type_check():
        tests_passed = False
        print("❌ Type checking failed!")

    print("=" * 50)
    if tests_passed:
        print("✅ All checks passed! Ready for deployment.")
        return 0
    else:
        print("❌ Some checks failed. Please fix the issues before deploying.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
