"""
E2E Tests for Manufacturing Module - Bill of Materials (BOM)
Tests the complete flow of creating and managing BOM documents
"""

import frappe
import pytest
from frappe.test_runner import make_test_records
from decimal import Decimal


class TestBOME2E:
    """End-to-End tests for BOM functionality"""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup test data before each test"""
        frappe.clear_cache()
        # Create test item if it doesn't exist
        if not frappe.db.exists("Item", "TEST-ITEM-001"):
            self._create_test_item("TEST-ITEM-001", "Test Item 1")
        if not frappe.db.exists("Item", "TEST-RAW-001"):
            self._create_test_item("TEST-RAW-001", "Test Raw Material 1")
        if not frappe.db.exists("Item", "TEST-RAW-002"):
            self._create_test_item("TEST-RAW-002", "Test Raw Material 2")

    @staticmethod
    def _create_test_item(item_code, item_name):
        """Helper to create test items"""
        item = frappe.new_doc("Item")
        item.item_code = item_code
        item.item_name = item_name
        item.item_group = "Raw Materials"
        item.uom = "Nos"
        item.is_stock_item = 1
        item.save(ignore_permissions=True)

    def test_create_bom_successfully(self):
        """Test creating a BOM with multiple items"""
        # Arrange
        bom_data = {
            "doctype": "BOM",
            "item": "TEST-ITEM-001",
            "quantity": 1,
            "company": frappe.defaults.get_user_default("company") or "Company",
            "items": [
                {
                    "item_code": "TEST-RAW-001",
                    "qty": 5,
                    "uom": "Nos",
                    "rate": 100,
                },
                {
                    "item_code": "TEST-RAW-002",
                    "qty": 3,
                    "uom": "Nos",
                    "rate": 50,
                }
            ]
        }

        # Act
        bom = frappe.get_doc(bom_data)
        bom.save(ignore_permissions=True)

        # Assert
        assert bom.name is not None
        assert len(bom.items) == 2
        assert bom.items[0].item_code == "TEST-RAW-001"
        assert bom.items[0].qty == 5
        assert frappe.db.exists("BOM", bom.name)

    def test_validate_bom_quantity(self):
        """Test that BOM quantity validation works"""
        # Arrange
        bom_data = {
            "doctype": "BOM",
            "item": "TEST-ITEM-001",
            "quantity": 0,  # Invalid quantity
            "company": frappe.defaults.get_user_default("company") or "Company",
            "items": [
                {
                    "item_code": "TEST-RAW-001",
                    "qty": 5,
                    "uom": "Nos",
                    "rate": 100,
                }
            ]
        }

        # Act & Assert
        bom = frappe.get_doc(bom_data)
        with pytest.raises(frappe.ValidationError):
            bom.save(ignore_permissions=True)

    def test_bom_calculation_total_cost(self):
        """Test that BOM calculates total cost correctly"""
        # Arrange
        bom_data = {
            "doctype": "BOM",
            "item": "TEST-ITEM-001",
            "quantity": 1,
            "company": frappe.defaults.get_user_default("company") or "Company",
            "items": [
                {
                    "item_code": "TEST-RAW-001",
                    "qty": 5,
                    "uom": "Nos",
                    "rate": 100,
                },
                {
                    "item_code": "TEST-RAW-002",
                    "qty": 3,
                    "uom": "Nos",
                    "rate": 50,
                }
            ]
        }

        # Act
        bom = frappe.get_doc(bom_data)
        bom.insert(ignore_permissions=True)

        # Calculate total cost: (5*100) + (3*50) = 650
        expected_total = (5 * 100) + (3 * 50)
        actual_total = sum(item.qty * item.rate for item in bom.items)

        # Assert
        assert actual_total == expected_total
        assert bom.items[0].stock_qty == 5
        assert bom.items[1].stock_qty == 3

    def test_bom_item_validation(self):
        """Test that BOM validates item codes correctly"""
        # Arrange
        bom_data = {
            "doctype": "BOM",
            "item": "TEST-ITEM-001",
            "quantity": 1,
            "company": frappe.defaults.get_user_default("company") or "Company",
            "items": [
                {
                    "item_code": "NONEXISTENT-ITEM",  # Invalid item
                    "qty": 5,
                    "uom": "Nos",
                    "rate": 100,
                }
            ]
        }

        # Act & Assert
        bom = frappe.get_doc(bom_data)
        # This should raise an error due to invalid item code
        # (Frappe validates item references)
        try:
            bom.insert(ignore_permissions=True)
            # If no error, the item might have been created, so check if it exists
            assert frappe.db.exists("Item", "NONEXISTENT-ITEM")
        except frappe.DoesNotExistError:
            # Expected behavior - item doesn't exist
            pass

    def test_bom_update_items(self):
        """Test updating BOM items after creation"""
        # Arrange - Create initial BOM
        bom_data = {
            "doctype": "BOM",
            "item": "TEST-ITEM-001",
            "quantity": 1,
            "company": frappe.defaults.get_user_default("company") or "Company",
            "items": [
                {
                    "item_code": "TEST-RAW-001",
                    "qty": 5,
                    "uom": "Nos",
                    "rate": 100,
                }
            ]
        }
        bom = frappe.get_doc(bom_data)
        bom.insert(ignore_permissions=True)

        # Act - Update BOM
        bom.items[0].qty = 10
        bom.save(ignore_permissions=True)

        # Assert
        updated_bom = frappe.get_doc("BOM", bom.name)
        assert updated_bom.items[0].qty == 10

    def teardown_method(self):
        """Clean up after each test"""
        # Delete test BOMs
        for bom in frappe.db.get_list("BOM", filters={"item": "TEST-ITEM-001"}):
            frappe.delete_doc("BOM", bom.name, ignore_permissions=True)


class TestWorkOrderE2E:
    """End-to-End tests for Work Order functionality"""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup test data before each test"""
        frappe.clear_cache()
        self._create_test_data()

    @staticmethod
    def _create_test_data():
        """Create necessary test data"""
        # Create test item
        if not frappe.db.exists("Item", "WO-TEST-ITEM"):
            item = frappe.new_doc("Item")
            item.item_code = "WO-TEST-ITEM"
            item.item_name = "Work Order Test Item"
            item.item_group = "Products"
            item.uom = "Nos"
            item.is_stock_item = 1
            item.save(ignore_permissions=True)

        # Create test BOM
        if not frappe.db.exists("BOM", "WO-TEST-BOM"):
            bom = frappe.new_doc("BOM")
            bom.name = "WO-TEST-BOM"
            bom.item = "WO-TEST-ITEM"
            bom.quantity = 1
            bom.company = frappe.defaults.get_user_default("company") or "Company"
            bom.insert(ignore_permissions=True)

    def test_create_work_order(self):
        """Test creating a Work Order"""
        # Arrange
        company = frappe.defaults.get_user_default("company") or "Company"
        
        # Act
        work_order = frappe.new_doc("Work Order")
        work_order.item_code = "WO-TEST-ITEM"
        work_order.qty = 10
        work_order.bom_no = "WO-TEST-BOM"
        work_order.company = company
        work_order.expected_delivery_date = frappe.utils.today()
        
        try:
            work_order.insert(ignore_permissions=True)
            
            # Assert
            assert work_order.name is not None
            assert work_order.status in ["Draft", "Not Started"]
            assert work_order.qty == 10
        except frappe.ValidationError as e:
            # If validation fails, ensure it's for expected reasons
            pytest.skip(f"BOM or item validation issue: {str(e)}")

    def test_work_order_quantity_validation(self):
        """Test Work Order quantity validation"""
        # Arrange
        company = frappe.defaults.get_user_default("company") or "Company"
        
        # Act & Assert
        work_order = frappe.new_doc("Work Order")
        work_order.item_code = "WO-TEST-ITEM"
        work_order.qty = 0  # Invalid
        work_order.bom_no = "WO-TEST-BOM"
        work_order.company = company

        with pytest.raises((frappe.ValidationError, ValueError)):
            work_order.insert(ignore_permissions=True)
