"""
Configuration file for E2E tests
Pytest configuration and fixtures
"""

import pytest
import os
import sys
from pathlib import Path

# Optionally allow forcing a local mock bench for E2E runs
if os.environ.get("E2E_FORCE_MOCK") == "1":
    try:
        from .mock_bench import get_mock_frappe
        sys.modules["frappe"] = get_mock_frappe()
    except Exception:
        pass

# Try to import frappe, but make it optional for initial setup
try:
    import frappe
    FRAPPE_AVAILABLE = True
except ImportError:
    FRAPPE_AVAILABLE = False
    frappe = None

FRAPPE_USABLE = FRAPPE_AVAILABLE and frappe is not None and hasattr(frappe, "connect") and hasattr(frappe, "clear_cache")


def _is_frappe_context_ready():
    if not FRAPPE_USABLE:
        return False

    if not getattr(frappe, "local", None):
        return False

    if not getattr(frappe, "db", None):
        return False

    return True


def _ensure_frappe_initialized():
    if not FRAPPE_USABLE:
        return

    try:
        if getattr(frappe, "db", None) is None or not getattr(frappe, "local", None):
            frappe.connect()
    except Exception as e:
        print(f"Warning: Could not connect to Frappe bench site: {e}")
        return

    if not getattr(frappe, "local", None) or not getattr(frappe, "db", None):
        print("Warning: Bench-ready frappe module imported, but local/db context is not initialized.")


def _clear_frappe_cache():
    if not _is_frappe_context_ready():
        return

    try:
        frappe.clear_cache()
    except Exception as e:
        print(f"Warning: Could not clear Frappe cache: {e}")


def pytest_configure(config):
    """Configure pytest environment and custom markers"""
    config.addinivalue_line(
        "markers", "manufacturing: Mark test as part of Manufacturing module"
    )
    config.addinivalue_line(
        "markers", "quality_management: Mark test as part of Quality Management module"
    )
    config.addinivalue_line(
        "markers", "shopping_cart: Mark test as part of Shopping Cart module"
    )
    config.addinivalue_line(
        "markers", "e2e: Mark test as end-to-end test"
    )

    _ensure_frappe_initialized()


def pytest_runtest_setup(item):
    if not _is_frappe_context_ready():
        pytest.skip(
            "Skipping E2E tests because a bench-ready Frappe installation with a valid site context is not available."
        )


@pytest.fixture(scope="session")
def frappe_test_db():
    """Setup Frappe test database"""
    _ensure_frappe_initialized()
    _clear_frappe_cache()
    return frappe.get_site_config() if FRAPPE_AVAILABLE else None


@pytest.fixture
def frappe_user(monkeypatch):
    """Set current frappe user for tests"""
    if FRAPPE_AVAILABLE and frappe is not None:
        monkeypatch.setattr(frappe.session, "user", "Administrator")
        frappe.set_user("Administrator")
    yield
    if FRAPPE_AVAILABLE and frappe is not None:
        frappe.set_user("Administrator")


@pytest.fixture(autouse=True)
def reset_frappe_cache():
    """Reset frappe cache before each test"""
    _clear_frappe_cache()
    yield
    _clear_frappe_cache()
