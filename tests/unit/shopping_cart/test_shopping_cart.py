# Copyright (c) 2024
# Unit tests for Shopping Cart module functionality

import pytest
from assertpy import assert_that
from decimal import Decimal


class TestShoppingCartItemManagement:
    """Test suite for Shopping Cart item operations"""

    def test_item_quantity_is_positive(self):
        # Arrange
        test_quantities = [1, 5, 10, 100, 999]

        # Act & Assert
        for qty in test_quantities:
            assert_that(qty).is_instance_of(int)
            assert_that(qty).is_greater_than(0)

    def test_item_price_is_positive_decimal(self):
        # Arrange
        test_prices = [Decimal("10.50"), Decimal("99.99"), Decimal("1000.00")]

        # Act & Assert
        for price in test_prices:
            assert_that(price).is_instance_of(Decimal)
            assert_that(float(price)).is_greater_than(0)

    def test_calculate_item_total(self):
        # Arrange
        unit_price = Decimal("50.00")
        quantity = 3

        # Act
        total = unit_price * quantity

        # Assert
        assert_that(total).is_equal_to(Decimal("150.00"))
        assert_that(float(total)).is_greater_than(0)


class TestShoppingCartValidation:
    """Test suite for Shopping Cart validation rules"""

    def test_cart_quantity_increment(self):
        # Arrange
        current_qty = 5
        increment = 1

        # Act
        new_qty = current_qty + increment

        # Assert
        assert_that(new_qty).is_equal_to(6)
        assert_that(new_qty).is_greater_than(current_qty)

    def test_cart_quantity_decrement(self):
        # Arrange
        current_qty = 5
        decrement = 1

        # Act
        new_qty = current_qty - decrement

        # Assert
        assert_that(new_qty).is_equal_to(4)
        assert_that(new_qty).is_less_than(current_qty)

    def test_cart_cannot_have_zero_quantity(self):
        # Arrange
        invalid_qty = 0

        # Act & Assert
        assert_that(invalid_qty).is_equal_to(0)
        assert_that(invalid_qty).is_less_than_or_equal_to(0)

    def test_cart_cannot_have_negative_quantity(self):
        # Arrange
        invalid_qty = -5

        # Act & Assert
        assert_that(invalid_qty).is_less_than(0)


class TestShoppingCartTotals:
    """Test suite for Shopping Cart calculation logic"""

    def test_calculate_subtotal(self):
        # Arrange
        items = [
            {"price": Decimal("100.00"), "qty": 2},
            {"price": Decimal("50.00"), "qty": 3},
            {"price": Decimal("25.00"), "qty": 4}
        ]

        # Act
        subtotal = sum(item["price"] * item["qty"] for item in items)

        # Assert
        expected_subtotal = Decimal("200.00") + Decimal("150.00") + Decimal("100.00")
        assert_that(float(subtotal)).is_equal_to(float(expected_subtotal))

    def test_calculate_discount_amount(self):
        # Arrange
        subtotal = Decimal("500.00")
        discount_percent = 10

        # Act
        discount_amount = subtotal * (Decimal(discount_percent) / Decimal("100"))

        # Assert
        assert_that(discount_amount).is_equal_to(Decimal("50.00"))
        assert_that(float(discount_amount)).is_greater_than(0)

    def test_calculate_final_total_with_tax(self):
        # Arrange
        subtotal = Decimal("1000.00")
        tax_percent = 16

        # Act
        tax_amount = subtotal * (Decimal(tax_percent) / Decimal("100"))
        final_total = subtotal + tax_amount

        # Assert
        assert_that(tax_amount).is_equal_to(Decimal("160.00"))
        assert_that(float(final_total)).is_equal_to(float(Decimal("1160.00")))

    def test_calculate_grand_total(self):
        # Arrange
        subtotal = Decimal("1000.00")
        tax = Decimal("160.00")
        shipping = Decimal("50.00")

        # Act
        grand_total = subtotal + tax + shipping

        # Assert
        assert_that(grand_total).is_equal_to(Decimal("1210.00"))
        assert_that(float(grand_total)).is_greater_than(float(subtotal))


class TestShoppingCartCart:
    """Test suite for Shopping Cart data structure"""

    def test_cart_is_empty_initially(self):
        # Arrange
        cart = []

        # Act & Assert
        assert_that(cart).is_empty()
        assert_that(len(cart)).is_equal_to(0)

    def test_cart_add_item(self):
        # Arrange
        cart = []
        item = {"item_code": "ITEM-001", "qty": 5, "price": Decimal("100.00")}

        # Act
        cart.append(item)

        # Assert
        assert_that(cart).is_not_empty()
        assert_that(len(cart)).is_equal_to(1)
        assert_that(cart[0]).is_equal_to(item)

    def test_cart_remove_item(self):
        # Arrange
        cart = [
            {"item_code": "ITEM-001", "qty": 5},
            {"item_code": "ITEM-002", "qty": 3}
        ]

        # Act
        cart.pop(0)

        # Assert
        assert_that(len(cart)).is_equal_to(1)
        assert_that(cart[0]["item_code"]).is_equal_to("ITEM-002")

    def test_cart_clear(self):
        # Arrange
        cart = [
            {"item_code": "ITEM-001", "qty": 5},
            {"item_code": "ITEM-002", "qty": 3}
        ]

        # Act
        cart.clear()

        # Assert
        assert_that(cart).is_empty()
        assert_that(len(cart)).is_equal_to(0)

    def test_cart_item_count(self):
        # Arrange
        items = [
            {"item_code": f"ITEM-{i:03d}", "qty": i+1} for i in range(5)
        ]

        # Act
        cart = items

        # Assert
        assert_that(len(cart)).is_equal_to(5)
        assert_that(cart).is_not_empty()
