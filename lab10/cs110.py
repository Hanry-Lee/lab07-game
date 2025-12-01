"""Simple test utilities for cs110."""
import subprocess
import sys

_passed = 0
_failed = 0

def expect(actual, expected):
    global _passed, _failed
    if actual == expected:
        _passed += 1
    else:
        _failed += 1
        print(f"FAIL: expected {expected}, got {actual}")

def summarize():
    print(f"\nTests: {_passed} passed, {_failed} failed")

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package, "-q"])
