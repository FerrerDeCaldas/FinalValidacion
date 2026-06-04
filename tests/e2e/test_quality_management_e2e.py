"""
E2E Tests for Quality Management Module
Tests the complete flow of Quality Procedures, Reviews, and Actions
"""

import frappe
import pytest
import time
from datetime import datetime


class TestQualityProcedureE2E:
    """End-to-End tests for Quality Procedure functionality"""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup test data before each test"""
        frappe.clear_cache()

    def test_create_quality_procedure(self):
        """Test creating a Quality Procedure"""
        # Arrange
        procedure_data = {
            "doctype": "Quality Procedure",
            "quality_procedure_name": "TEST-PROCEDURE-001",
            "is_group": 0,
            "parent_quality_procedure": None,
            "process_owner": frappe.session.user,
            "processes": []
        }

        # Act
        procedure = frappe.get_doc(procedure_data)
        procedure.insert(ignore_permissions=True)

        # Assert
        assert procedure.name is not None
        assert procedure.quality_procedure_name == "TEST-PROCEDURE-001"
        assert frappe.db.exists("Quality Procedure", procedure.name)

    def test_quality_procedure_with_processes(self):
        """Test creating Quality Procedure with sub-processes"""
        # Arrange - Create parent procedure
        parent_proc = frappe.new_doc("Quality Procedure")
        parent_proc.quality_procedure_name = "PARENT-PROCEDURE-001"
        parent_proc.is_group = 1
        parent_proc.process_owner = frappe.session.user
        parent_proc.insert(ignore_permissions=True)

        # Create child procedure
        child_proc = frappe.new_doc("Quality Procedure")
        child_proc.quality_procedure_name = "CHILD-PROCEDURE-001"
        child_proc.is_group = 0
        child_proc.process_owner = frappe.session.user
        child_proc.parent_quality_procedure = parent_proc.name
        child_proc.insert(ignore_permissions=True)

        # Assert
        assert child_proc.parent_quality_procedure == parent_proc.name
        parent_doc = frappe.get_doc("Quality Procedure", parent_proc.name)
        assert parent_doc.is_group == 1

    def test_quality_procedure_validation(self):
        """Test Quality Procedure validation"""
        # Arrange & Act - Try to create procedure with empty name
        procedure = frappe.new_doc("Quality Procedure")
        procedure.quality_procedure_name = ""
        procedure.is_group = 0
        procedure.process_owner = frappe.session.user

        # Assert
        with pytest.raises((frappe.ValidationError, frappe.MandatoryError)):
            procedure.insert(ignore_permissions=True)

    def test_quality_procedure_update(self):
        """Test updating Quality Procedure"""
        # Arrange - Create procedure
        procedure = frappe.new_doc("Quality Procedure")
        procedure.quality_procedure_name = "UPDATE-TEST-PROC"
        procedure.is_group = 0
        procedure.process_owner = frappe.session.user
        procedure.insert(ignore_permissions=True)

        # Act - Update procedure
        procedure.is_group = 1
        procedure.save(ignore_permissions=True)

        # Assert
        updated = frappe.get_doc("Quality Procedure", procedure.name)
        assert updated.is_group == 1


class TestQualityReviewE2E:
    """End-to-End tests for Quality Review functionality"""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup test data before each test"""
        frappe.clear_cache()
        self._create_test_item()

    @staticmethod
    def _create_test_item():
        """Create test item for quality review"""
        if not frappe.db.exists("Item", "QR-TEST-ITEM"):
            item = frappe.new_doc("Item")
            item.item_code = "QR-TEST-ITEM"
            item.item_name = "Quality Review Test Item"
            item.item_group = "Raw Materials"
            item.uom = "Nos"
            item.is_stock_item = 1
            item.save(ignore_permissions=True)

    def test_create_quality_review(self):
        """Test creating a Quality Review"""
        try:
            # Arrange
            review_data = {
                "doctype": "Quality Review",
                "item_code": "QR-TEST-ITEM",
                "status": "Not Reviewed",
                "reviewer": frappe.session.user,
            }

            # Act
            review = frappe.get_doc(review_data)
            review.insert(ignore_permissions=True)

            # Assert
            assert review.name is not None
            assert review.item_code == "QR-TEST-ITEM"
            assert review.status == "Not Reviewed"
        except frappe.DoesNotExistError:
            # Quality Review might not be fully configured
            pytest.skip("Quality Review not available in this setup")

    def test_quality_review_with_objectives(self):
        """Test Quality Review with objectives"""
        try:
            # Arrange
            review = frappe.new_doc("Quality Review")
            review.item_code = "QR-TEST-ITEM"
            review.status = "Not Reviewed"
            review.reviewer = frappe.session.user

            # Add objective
            review.append("objectives", {
                "doctype": "Quality Review Objective",
                "objective": "Test Objective 1"
            })

            # Act
            review.insert(ignore_permissions=True)

            # Assert
            assert len(review.objectives) > 0
            assert review.objectives[0].objective == "Test Objective 1"
        except frappe.DoesNotExistError:
            pytest.skip("Quality Review not available in this setup")

    def test_quality_review_status_update(self):
        """Test updating Quality Review status"""
        try:
            # Arrange
            review = frappe.new_doc("Quality Review")
            review.item_code = "QR-TEST-ITEM"
            review.status = "Not Reviewed"
            review.reviewer = frappe.session.user
            review.insert(ignore_permissions=True)

            # Act - Update status
            review.status = "Reviewed"
            review.save(ignore_permissions=True)

            # Assert
            updated = frappe.get_doc("Quality Review", review.name)
            assert updated.status == "Reviewed"
        except frappe.DoesNotExistError:
            pytest.skip("Quality Review not available in this setup")


class TestQualityActionE2E:
    """End-to-End tests for Quality Action functionality"""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup test data before each test"""
        frappe.clear_cache()

    def test_create_quality_action(self):
        """Test creating a Quality Action"""
        try:
            # Arrange
            action_data = {
                "doctype": "Quality Action",
                "title": "TEST ACTION 001",
                "status": "Open",
                "owner": frappe.session.user,
            }

            # Act
            action = frappe.get_doc(action_data)
            action.insert(ignore_permissions=True)

            # Assert
            assert action.name is not None
            assert action.title == "TEST ACTION 001"
            assert action.status == "Open"
        except frappe.DoesNotExistError:
            pytest.skip("Quality Action not available in this setup")

    def test_quality_action_with_resolution(self):
        """Test Quality Action with resolution"""
        try:
            # Arrange
            action = frappe.new_doc("Quality Action")
            action.title = "TEST ACTION 002"
            action.status = "Open"
            action.owner = frappe.session.user

            # Add resolution
            action.append("resolutions", {
                "doctype": "Quality Action Resolution",
                "resolution_details": "Fix applied"
            })

            # Act
            action.insert(ignore_permissions=True)

            # Assert
            assert len(action.resolutions) > 0
            assert action.resolutions[0].resolution_details == "Fix applied"
        except frappe.DoesNotExistError:
            pytest.skip("Quality Action not available in this setup")

    def test_quality_action_status_update(self):
        """Test Quality Action status workflow"""
        try:
            # Arrange
            action = frappe.new_doc("Quality Action")
            action.title = "TEST ACTION 003"
            action.status = "Open"
            action.owner = frappe.session.user
            action.insert(ignore_permissions=True)

            # Act - Change status
            action.status = "Closed"
            action.save(ignore_permissions=True)

            # Assert
            updated = frappe.get_doc("Quality Action", action.name)
            assert updated.status == "Closed"
        except frappe.DoesNotExistError:
            pytest.skip("Quality Action not available in this setup")


class TestQualityGoalE2E:
    """End-to-End tests for Quality Goal functionality"""

    def test_create_quality_goal(self):
        """Test creating a Quality Goal"""
        try:
            # Arrange
            goal_data = {
                "doctype": "Quality Goal",
                "title": "TEST GOAL 001",
                "owner": frappe.session.user,
            }

            # Act
            goal = frappe.get_doc(goal_data)
            goal.insert(ignore_permissions=True)

            # Assert
            assert goal.name is not None
            assert goal.title == "TEST GOAL 001"
        except frappe.DoesNotExistError:
            pytest.skip("Quality Goal not available in this setup")

    def test_quality_goal_with_objectives(self):
        """Test Quality Goal with objectives"""
        try:
            # Arrange
            goal = frappe.new_doc("Quality Goal")
            goal.title = "TEST GOAL 002"
            goal.owner = frappe.session.user

            # Add objective
            goal.append("objectives", {
                "doctype": "Quality Goal Objective",
                "objective": "Achieve 99% quality"
            })

            # Act
            goal.insert(ignore_permissions=True)

            # Assert
            assert len(goal.objectives) > 0
            assert goal.objectives[0].objective == "Achieve 99% quality"
        except frappe.DoesNotExistError:
            pytest.skip("Quality Goal not available in this setup")
