# Copyright (c) 2024
# Shared pytest configuration for all tests

import sys
import pytest
from unittest.mock import Mock, MagicMock, patch

# Auto-mock frappe module only when Frappe is not installed or not bench-ready.
# This allows unit tests to run without a full Frappe bench installation,
# while e2e tests can still use a real frappe package when available.
try:
    import frappe  # noqa: F401
    FRAPPE_INSTALLED = hasattr(frappe, 'connect') and hasattr(frappe, 'clear_cache')
except ImportError:
    FRAPPE_INSTALLED = False

if not FRAPPE_INSTALLED:
    sys.modules['frappe'] = MagicMock()
    sys.modules['frappe.model'] = MagicMock()
    sys.modules['frappe.model.document'] = MagicMock()
    sys.modules['frappe.model.mapper'] = MagicMock()
    sys.modules['frappe.query_builder'] = MagicMock()
    sys.modules['frappe.query_builder.functions'] = MagicMock()
    sys.modules['frappe.utils'] = MagicMock()
    sys.modules['frappe.utils.nestedset'] = MagicMock()
    sys.modules['frappe.core'] = MagicMock()
    sys.modules['frappe.core.doctype'] = MagicMock()
    sys.modules['frappe.core.doctype.version'] = MagicMock()
    sys.modules['frappe.core.doctype.version.version'] = MagicMock()
    sys.modules['frappe.website'] = MagicMock()
    sys.modules['frappe.website.website_generator'] = MagicMock()

    # Create frappe module mock with proper attributes
    frappe_mock = MagicMock()
    frappe_mock.ValidationError = Exception
    frappe_mock._ = lambda x: x
    frappe_mock.get_value = MagicMock(return_value=None)
    frappe_mock.db = MagicMock()
    frappe_mock.db.exists = MagicMock(return_value=True)
    frappe_mock.db.get_value = MagicMock(return_value=None)
    frappe_mock.bold = lambda x: f"**{x}**"
    frappe_mock.throw = lambda x: None

    sys.modules['frappe'] = frappe_mock


@pytest.fixture
def mock_frappe():
    """Mock frappe module for testing"""
    with patch('frappe') as mock_frappe:
        mock_frappe.ValidationError = Exception
        mock_frappe._ = lambda x: x
        mock_frappe.get_value = MagicMock()
        mock_frappe.db = MagicMock()
        mock_frappe.db.exists = MagicMock(return_value=True)
        mock_frappe.db.get_value = MagicMock(return_value=None)
        yield mock_frappe


@pytest.fixture
def mock_document():
    """Mock Document class for testing"""
    doc = MagicMock()
    doc.name = "TEST-001"
    doc.doctype = "Test DocType"
    doc.db_insert = MagicMock()
    doc.db_update = MagicMock()
    return doc


@pytest.fixture
def mock_logger():
    """Mock logger for test output"""
    logger = MagicMock()
    return logger
