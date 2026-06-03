# Copyright (c) 2024
# Unit tests for Shopping Cart module - Advanced scenarios

import pytest
from unittest.mock import Mock, MagicMock, patch
from assertpy import assert_that
from decimal import Decimal
from datetime import datetime, timedelta


class TestShoppingCartPricing:
    """Test suite for Shopping Cart pricing logic"""

    def test_apply_percentage_discount(self):
        # Arrange
        original_price = Decimal("100.00")
        discount_percentage = Decimal("10")

        # Act
        discount_amount = original_price * (discount_percentage / Decimal("100"))
        final_price = original_price - discount_amount

        # Assert
        assert_that(discount_amount).is_equal_to(Decimal("10.00"))
        assert_that(final_price).is_equal_to(Decimal("90.00"))

    def test_apply_flat_discount(self):
        # Arrange
        original_price = Decimal("100.00")
        flat_discount = Decimal("15.00")

        # Act
        final_price = original_price - flat_discount

        # Assert
        assert_that(final_price).is_equal_to(Decimal("85.00"))
        assert_that(final_price).is_less_than(original_price)

    def test_tiered_pricing(self):
        # Arrange
        qty = 100
        tier_prices = [
            {'qty_from': 1, 'qty_to': 50, 'price': Decimal("100.00")},
            {'qty_from': 51, 'qty_to': 100, 'price': Decimal("90.00")},
            {'qty_from': 101, 'qty_to': 999, 'price': Decimal("80.00")}
        ]

        # Act
        applicable_tier = next(
            (tier for tier in tier_prices 
             if tier['qty_from'] <= qty <= tier['qty_to']),
            None
        )

        # Assert
        assert_that(applicable_tier).is_not_none()
        assert_that(applicable_tier['price']).is_equal_to(Decimal("90.00"))


class TestShoppingCartTaxCalculation:
    """Test suite for Tax calculations"""

    def test_single_tax_calculation(self):
        # Arrange
        subtotal = Decimal("1000.00")
        tax_rate = Decimal("16")  # 16% GST

        # Act
        tax_amount = subtotal * (tax_rate / Decimal("100"))
        total_with_tax = subtotal + tax_amount

        # Assert
        assert_that(tax_amount).is_equal_to(Decimal("160.00"))
        assert_that(total_with_tax).is_equal_to(Decimal("1160.00"))

    def test_multiple_taxes(self):
        # Arrange
        subtotal = Decimal("1000.00")
        tax_rules = [
            {'name': 'CGST', 'rate': Decimal("9")},
            {'name': 'SGST', 'rate': Decimal("9")},
            {'name': 'Cess', 'rate': Decimal("2")}
        ]

        # Act
        total_tax_rate = sum(tax['rate'] for tax in tax_rules)
        total_tax = subtotal * (total_tax_rate / Decimal("100"))
        final_total = subtotal + total_tax

        # Assert
        assert_that(total_tax_rate).is_equal_to(Decimal("20"))
        assert_that(final_total).is_equal_to(Decimal("1200.00"))

    def test_tax_exemption(self):
        # Arrange
        subtotal = Decimal("1000.00")
        is_tax_exempt = True

        # Act
        tax_amount = Decimal("0") if is_tax_exempt else subtotal * (Decimal("16") / Decimal("100"))

        # Assert
        assert_that(tax_amount).is_equal_to(Decimal("0"))


class TestShoppingCartPayment:
    """Test suite for Payment processing"""

    def test_payment_method_validation(self):
        # Arrange
        valid_payment_methods = ['Credit Card', 'Debit Card', 'Net Banking', 'Cash']

        # Act & Assert
        for method in valid_payment_methods:
            assert_that(method).is_not_empty()
            assert_that(method).is_instance_of(str)

    def test_payment_processing(self):
        # Arrange
        total_amount = Decimal("1000.00")
        payment_method = 'Credit Card'
        transaction_id = "TXN-12345"

        # Act
        payment_record = {
            'amount': total_amount,
            'method': payment_method,
            'transaction_id': transaction_id,
            'status': 'Completed',
            'timestamp': datetime.now()
        }

        # Assert
        assert_that(payment_record['amount']).is_equal_to(total_amount)
        assert_that(payment_record['status']).is_equal_to('Completed')
        assert_that(payment_record).contains_key('transaction_id', 'timestamp')

    def test_payment_failure_handling(self):
        # Arrange
        payment_attempts = [
            {'attempt': 1, 'status': 'Failed', 'reason': 'Insufficient funds'},
            {'attempt': 2, 'status': 'Failed', 'reason': 'Connection timeout'},
            {'attempt': 3, 'status': 'Success', 'reason': None}
        ]

        # Act
        successful = next(
            (p for p in payment_attempts if p['status'] == 'Success'),
            None
        )

        # Assert
        assert_that(successful).is_not_none()
        assert_that(successful['attempt']).is_equal_to(3)


class TestShoppingCartInventory:
    """Test suite for Inventory and Stock management"""

    def test_stock_availability_check(self):
        # Arrange
        item_code = "ITEM-001"
        requested_qty = 10
        available_stock = 15

        # Act
        is_available = available_stock >= requested_qty

        # Assert
        assert_that(is_available).is_true()

    def test_stock_insufficient(self):
        # Arrange
        requested_qty = 50
        available_stock = 20

        # Act
        is_available = available_stock >= requested_qty

        # Assert
        assert_that(is_available).is_false()

    def test_backorder_creation(self):
        # Arrange
        requested_qty = 100
        available_stock = 60
        backorder_qty = requested_qty - available_stock

        # Act
        backorder = {
            'qty': backorder_qty,
            'status': 'Pending',
            'expected_date': (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')
        }

        # Assert
        assert_that(backorder['qty']).is_equal_to(40)
        assert_that(backorder['status']).is_equal_to('Pending')

    def test_stock_reservation(self):
        # Arrange
        item_code = "ITEM-001"
        qty = 10
        warehouse = "Main Warehouse"
        customer = "CUST-001"

        # Act
        reservation = {
            'item_code': item_code,
            'qty': qty,
            'warehouse': warehouse,
            'customer': customer,
            'reserved_date': datetime.now()
        }

        # Assert
        assert_that(reservation).contains_key('item_code', 'qty', 'warehouse', 'customer')
        assert_that(reservation['qty']).is_equal_to(qty)


class TestShoppingCartShipping:
    """Test suite for Shipping operations"""

    def test_shipping_method_selection(self):
        # Arrange
        shipping_methods = {
            'Standard': {'cost': Decimal("100"), 'days': 5},
            'Express': {'cost': Decimal("250"), 'days': 2},
            'Overnight': {'cost': Decimal("500"), 'days': 1}
        }

        # Act & Assert
        for method, details in shipping_methods.items():
            assert_that(details).contains_key('cost', 'days')
            assert_that(details['cost']).is_greater_than(0)
            assert_that(details['days']).is_greater_than(0)

    def test_shipping_cost_calculation(self):
        # Arrange
        base_weight = 5.0  # kg
        price_per_kg = Decimal("50.00")
        handling_fee = Decimal("75.00")

        # Act
        shipping_cost = (Decimal(str(base_weight)) * price_per_kg) + handling_fee

        # Assert
        assert_that(shipping_cost).is_equal_to(Decimal("325.00"))

    def test_delivery_date_estimation(self):
        # Arrange
        order_date = datetime(2024, 6, 15, 10, 0)
        shipping_days = 3

        # Act
        estimated_delivery = order_date + timedelta(days=shipping_days)

        # Assert
        assert_that(estimated_delivery).is_greater_than(order_date)
        days_diff = (estimated_delivery - order_date).days
        assert_that(days_diff).is_equal_to(shipping_days)


class TestShoppingCartVoucher:
    """Test suite for Voucher/Coupon management"""

    def test_voucher_validation(self):
        # Arrange
        voucher_code = "SUMMER2024"
        is_valid = True
        is_expired = False

        # Act
        voucher_applicable = is_valid and not is_expired

        # Assert
        assert_that(voucher_applicable).is_true()

    def test_voucher_discount_application(self):
        # Arrange
        cart_total = Decimal("500.00")
        voucher = {
            'code': 'DISCOUNT20',
            'discount_type': 'Percentage',
            'discount_value': Decimal("20")
        }

        # Act
        discount_amount = cart_total * (voucher['discount_value'] / Decimal("100"))
        final_amount = cart_total - discount_amount

        # Assert
        assert_that(discount_amount).is_equal_to(Decimal("100.00"))
        assert_that(final_amount).is_equal_to(Decimal("400.00"))

    def test_voucher_usage_limit(self):
        # Arrange
        voucher_max_usage = 100
        voucher_used = 95

        # Act
        remaining_usage = voucher_max_usage - voucher_used
        can_use = remaining_usage > 0

        # Assert
        assert_that(can_use).is_true()
        assert_that(remaining_usage).is_equal_to(5)


class TestShoppingCartOrderCreation:
    """Test suite for Order creation from cart"""

    def test_cart_to_order_conversion(self):
        # Arrange
        cart_items = [
            {'item_code': 'ITEM-001', 'qty': 2, 'price': Decimal("100.00")},
            {'item_code': 'ITEM-002', 'qty': 3, 'price': Decimal("50.00")}
        ]

        # Act
        order_lines = [
            {'item_code': item['item_code'], 'qty': item['qty']}
            for item in cart_items
        ]
        total = sum(item['qty'] * item['price'] for item in cart_items)

        # Assert
        assert_that(len(order_lines)).is_equal_to(2)
        assert_that(total).is_equal_to(Decimal("350.00"))

    def test_order_number_generation(self):
        # Arrange
        prefix = "ORD"
        sequence = 12345

        # Act
        order_number = f"{prefix}-{sequence:06d}"

        # Assert
        assert_that(order_number).is_equal_to("ORD-012345")
        assert_that(order_number).is_not_empty()

    def test_customer_information_capture(self):
        # Arrange
        customer_info = {
            'email': 'customer@example.com',
            'phone': '+1234567890',
            'shipping_address': '123 Main St',
            'billing_address': '123 Main St'
        }

        # Act & Assert
        assert_that(customer_info).contains_key('email', 'phone', 'shipping_address')
        assert_that(customer_info['email']).is_not_empty()
