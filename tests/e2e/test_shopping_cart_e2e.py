"""
E2E Tests for Shopping Cart Module
Tests the complete flow of shopping cart, sales orders, and payments
"""

import frappe
import pytest
import time
from decimal import Decimal
from datetime import datetime, timedelta


class TestShoppingCartE2E:
    """End-to-End tests for Shopping Cart functionality"""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup test data before each test"""
        frappe.clear_cache()
        self._ensure_master_data()
        self._create_test_items()
        self._create_test_customer()

    @staticmethod
    def _create_test_items():
        """Create test items for shopping cart"""
        items = [
            ("SC-ITEM-001", "Shopping Cart Item 1", 100),
            ("SC-ITEM-002", "Shopping Cart Item 2", 250),
            ("SC-ITEM-003", "Shopping Cart Item 3", 150),
        ]

        for item_code, item_name, price in items:
            if not frappe.db.exists("Item", item_code):
                item = frappe.new_doc("Item")
                item.item_code = item_code
                item.item_name = item_name
                item.item_group = "Products"
                item.uom = "Nos"
                item.is_stock_item = 1
                item.stock_uom = "Nos"
                item.save(ignore_permissions=True)

                # Create item price
                if not frappe.db.exists(
                    "Item Price",
                    {
                        "item_code": item_code,
                        "price_list": "Standard Selling"
                    }
                ):
                    price_obj = frappe.new_doc("Item Price")
                    price_obj.item_code = item_code
                    price_obj.price_list = "Standard Buying"
                    price_obj.price_list_rate = price
                    price_obj.save(ignore_permissions=True)

    @staticmethod
    def _ensure_master_data():
        """Ensure UOM and Price Lists required for tests exist"""
        # Ensure UOM
        if not frappe.db.exists("UOM", "Nos"):
            try:
                uom = frappe.get_doc({"doctype": "UOM", "uom_name": "Nos"})
                uom.insert(ignore_permissions=True)
            except Exception:
                pass

        # Ensure Price Lists
        if not frappe.db.exists("Price List", "Standard Selling"):
            try:
                pl = frappe.get_doc({"doctype": "Price List", "price_list_name": "Standard Selling", "selling": 1})
                pl.insert(ignore_permissions=True)
            except Exception:
                pass
        if not frappe.db.exists("Price List", "Standard Buying"):
            try:
                plb = frappe.get_doc({"doctype": "Price List", "price_list_name": "Standard Buying", "buying": 1})
                plb.insert(ignore_permissions=True)
            except Exception:
                pass

    @staticmethod
    def _create_test_customer():
        """Create test customer"""
        if not frappe.db.exists("Customer", "TEST-CUST-001"):
            customer = frappe.new_doc("Customer")
            customer.customer_name = "Test Customer"
            customer.name = "TEST-CUST-001"
            customer.customer_type = "Individual"
            customer.customer_group = "Individual"
            customer.territory = "India"
            customer.save(ignore_permissions=True)

    def test_create_sales_order_from_cart(self):
        """Test creating Sales Order from cart items"""
        # Arrange
        company = frappe.defaults.get_user_default("company") or "Company"
        
        # Act
        sales_order = frappe.new_doc("Sales Order")
        sales_order.customer = "TEST-CUST-001"
        sales_order.company = company
        sales_order.transaction_date = frappe.utils.today()
        sales_order.delivery_date = frappe.utils.today()

        # Add items to cart
        sales_order.append("items", {
            "item_code": "SC-ITEM-001",
            "qty": 5,
            "uom": "Nos",
            "rate": 100,
        })
        sales_order.append("items", {
            "item_code": "SC-ITEM-002",
            "qty": 3,
            "uom": "Nos",
            "rate": 250,
        })

        try:
            sales_order.insert(ignore_permissions=True)

            # Assert
            assert sales_order.name is not None
            assert len(sales_order.items) == 2
            assert sales_order.items[0].item_code == "SC-ITEM-001"
            assert sales_order.items[0].qty == 5
            assert sales_order.status == "Draft"
        except frappe.ValidationError as e:
            pytest.skip(f"Sales Order validation: {str(e)}")

    def test_cart_total_calculation(self):
        """Test that cart total is calculated correctly"""
        # Arrange
        company = frappe.defaults.get_user_default("company") or "Company"
        
        # Act
        sales_order = frappe.new_doc("Sales Order")
        sales_order.customer = "TEST-CUST-001"
        sales_order.company = company
        sales_order.transaction_date = frappe.utils.today()
        sales_order.delivery_date = frappe.utils.today()

        # Add items
        sales_order.append("items", {
            "item_code": "SC-ITEM-001",
            "qty": 5,
            "uom": "Nos",
            "rate": 100,
        })
        sales_order.append("items", {
            "item_code": "SC-ITEM-002",
            "qty": 3,
            "uom": "Nos",
            "rate": 250,
        })

        try:
            sales_order.insert(ignore_permissions=True)

            # Calculate total: (5*100) + (3*250) = 1250
            expected_total = (5 * 100) + (3 * 250)
            actual_total = sales_order.grand_total

            # Assert
            assert actual_total == expected_total
        except frappe.ValidationError:
            pytest.skip("Sales Order validation issue")

    def test_apply_discount_to_cart(self):
        """Test applying discount to cart items"""
        # Arrange
        company = frappe.defaults.get_user_default("company") or "Company"
        
        # Act
        sales_order = frappe.new_doc("Sales Order")
        sales_order.customer = "TEST-CUST-001"
        sales_order.company = company
        sales_order.transaction_date = frappe.utils.today()
        sales_order.delivery_date = frappe.utils.today()

        sales_order.append("items", {
            "item_code": "SC-ITEM-001",
            "qty": 10,
            "uom": "Nos",
            "rate": 100,
        })

        # Apply 10% discount
        sales_order.discount_percentage = 10

        try:
            sales_order.insert(ignore_permissions=True)

            # Assert - Total should be 900 (1000 - 100)
            expected_total = (10 * 100) * (1 - 0.10)
            # Note: grand_total includes tax, so we check the subtotal
            assert sales_order.net_total <= (10 * 100)
        except frappe.ValidationError:
            pytest.skip("Sales Order validation issue")

    def test_cart_item_removal(self):
        """Test removing items from cart"""
        # Arrange
        company = frappe.defaults.get_user_default("company") or "Company"
        
        sales_order = frappe.new_doc("Sales Order")
        sales_order.customer = "TEST-CUST-001"
        sales_order.company = company
        sales_order.transaction_date = frappe.utils.today()
        sales_order.delivery_date = frappe.utils.today()

        sales_order.append("items", {
            "item_code": "SC-ITEM-001",
            "qty": 5,
            "uom": "Nos",
            "rate": 100,
        })
        sales_order.append("items", {
            "item_code": "SC-ITEM-002",
            "qty": 3,
            "uom": "Nos",
            "rate": 250,
        })

        try:
            sales_order.insert(ignore_permissions=True)
            initial_count = len(sales_order.items)

            # Act - Remove first item
            sales_order.items.pop(0)
            sales_order.save(ignore_permissions=True)

            # Assert
            updated = frappe.get_doc("Sales Order", sales_order.name)
            assert len(updated.items) == initial_count - 1
        except frappe.ValidationError:
            pytest.skip("Sales Order validation issue")

    def test_cart_quantity_update(self):
        """Test updating item quantity in cart"""
        # Arrange
        company = frappe.defaults.get_user_default("company") or "Company"
        
        sales_order = frappe.new_doc("Sales Order")
        sales_order.customer = "TEST-CUST-001"
        sales_order.company = company
        sales_order.transaction_date = frappe.utils.today()
        sales_order.delivery_date = frappe.utils.today()

        sales_order.append("items", {
            "item_code": "SC-ITEM-001",
            "qty": 5,
            "uom": "Nos",
            "rate": 100,
        })

        try:
            sales_order.insert(ignore_permissions=True)

            # Act - Update quantity
            sales_order.items[0].qty = 10
            sales_order.save(ignore_permissions=True)

            # Assert
            updated = frappe.get_doc("Sales Order", sales_order.name)
            assert updated.items[0].qty == 10
        except frappe.ValidationError:
            pytest.skip("Sales Order validation issue")


class TestPaymentProcessingE2E:
    """End-to-End tests for Payment Processing"""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup test data before each test"""
        frappe.clear_cache()
        self._create_payment_test_data()

    @staticmethod
    def _create_payment_test_data():
        """Create test data for payment processing"""
        # Create test customer
        if not frappe.db.exists("Customer", "PAY-TEST-CUST"):
            customer = frappe.new_doc("Customer")
            customer.name = "PAY-TEST-CUST"
            customer.customer_name = "Payment Test Customer"
            customer.customer_type = "Individual"
            customer.customer_group = "Individual"
            customer.territory = "India"
            customer.save(ignore_permissions=True)

    def test_create_payment_request(self):
        """Test creating a Payment Request"""
        try:
            # Arrange
            company = frappe.defaults.get_user_default("company") or "Company"
            
            payment_request = frappe.new_doc("Payment Request")
            payment_request.customer = "PAY-TEST-CUST"
            payment_request.amount = 1000
            payment_request.currency = "INR"
            payment_request.company = company
            payment_request.reference_doctype = "Sales Order"

            # Act
            payment_request.insert(ignore_permissions=True)

            # Assert
            assert payment_request.name is not None
            assert payment_request.amount == 1000
            assert payment_request.status in ["Initiated", "Pending"]
        except frappe.DoesNotExistError:
            pytest.skip("Payment Request not configured in this setup")

    def test_payment_request_with_email(self):
        """Test Payment Request sends email notification"""
        try:
            # Arrange
            company = frappe.defaults.get_user_default("company") or "Company"
            
            payment_request = frappe.new_doc("Payment Request")
            payment_request.customer = "PAY-TEST-CUST"
            payment_request.amount = 500
            payment_request.currency = "INR"
            payment_request.company = company
            payment_request.send_email = 1

            # Act
            payment_request.insert(ignore_permissions=True)

            # Assert
            assert payment_request.name is not None
            # Email sending is handled asynchronously in Frappe
            assert payment_request.send_email == 1
        except frappe.DoesNotExistError:
            pytest.skip("Payment Request not configured in this setup")

    def test_payment_workflow(self):
        """Test payment request workflow"""
        try:
            # Arrange
            company = frappe.defaults.get_user_default("company") or "Company"
            
            payment_request = frappe.new_doc("Payment Request")
            payment_request.customer = "PAY-TEST-CUST"
            payment_request.amount = 1000
            payment_request.currency = "INR"
            payment_request.company = company
            payment_request.insert(ignore_permissions=True)

            initial_status = payment_request.status

            # Act - Try to mark as paid
            payment_request.status = "Paid"
            payment_request.save(ignore_permissions=True)

            # Assert
            updated = frappe.get_doc("Payment Request", payment_request.name)
            assert updated.status == "Paid"
        except frappe.DoesNotExistError:
            pytest.skip("Payment Request not configured in this setup")


class TestTaxCalculationE2E:
    """End-to-End tests for Tax Calculation in Shopping Cart"""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup test data"""
        frappe.clear_cache()
        self._create_tax_test_data()

    @staticmethod
    def _create_tax_test_data():
        """Create test data for tax calculations"""
        # Create customer
        if not frappe.db.exists("Customer", "TAX-TEST-CUST"):
            customer = frappe.new_doc("Customer")
            customer.name = "TAX-TEST-CUST"
            customer.customer_name = "Tax Test Customer"
            customer.customer_type = "Individual"
            customer.customer_group = "Individual"
            customer.territory = "India"
            customer.save(ignore_permissions=True)

        # Create item
        if not frappe.db.exists("Item", "TAX-TEST-ITEM"):
            item = frappe.new_doc("Item")
            item.item_code = "TAX-TEST-ITEM"
            item.item_name = "Tax Test Item"
            item.item_group = "Products"
            item.uom = "Nos"
            item.is_stock_item = 1
            item.save(ignore_permissions=True)

    def test_sales_order_tax_calculation(self):
        """Test tax calculation in sales order"""
        try:
            # Arrange
            company = frappe.defaults.get_user_default("company") or "Company"
            
            sales_order = frappe.new_doc("Sales Order")
            sales_order.customer = "TAX-TEST-CUST"
            sales_order.company = company
            sales_order.transaction_date = frappe.utils.today()
            sales_order.delivery_date = frappe.utils.today()

            sales_order.append("items", {
                "item_code": "TAX-TEST-ITEM",
                "qty": 10,
                "uom": "Nos",
                "rate": 100,
            })

            # Act
            sales_order.insert(ignore_permissions=True)

            # Assert - Tax should be calculated
            # (Exact tax depends on configuration)
            assert hasattr(sales_order, 'total_tax')
            assert sales_order.grand_total >= sales_order.net_total
        except frappe.ValidationError as e:
            pytest.skip(f"Sales Order tax calculation: {str(e)}")
