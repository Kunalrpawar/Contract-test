"""
Pytest Configuration and Test Running Script
"""

import subprocess
import sys
import os


def run_tests():
    """Run all tests with coverage reporting"""
    
    print("=" * 80)
    print("Running ContractIQ Test Suite")
    print("=" * 80)
    
    # Unit Tests
    print("\n1. Running Unit Tests...")
    print("-" * 80)
    result = subprocess.run([
        sys.executable, "-m", "pytest",
        "tests/",
        "-v",
        "--tb=short",
        "-k", "not load_test"
    ])
    
    if result.returncode != 0:
        print("\n✗ Unit tests failed!")
        return False
    
    print("\n✓ Unit tests passed!")
    
    # Coverage Report
    print("\n2. Running Tests with Coverage...")
    print("-" * 80)
    result = subprocess.run([
        sys.executable, "-m", "pytest",
        "tests/",
        "--cov=app",
        "--cov-report=html",
        "--cov-report=term",
        "-k", "not load_test"
    ])
    
    print("\nCoverage report generated in htmlcov/index.html")
    
    return True


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
