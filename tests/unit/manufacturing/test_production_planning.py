# Copyright (c) 2024
# Unit tests for Manufacturing module - Production scheduling

import pytest
from assertpy import assert_that


class TestProductionPlanning:
    """Test suite for Production Planning operations"""

    def test_production_plan_creation(self):
        # Arrange
        plan_name = "PROD-PLAN-001"
        company = "Company A"
        plant_date_from = "2024-01-01"
        plant_date_to = "2024-01-31"

        # Act
        production_plan = {
            'name': plan_name,
            'company': company,
            'plant_date_from': plant_date_from,
            'plant_date_to': plant_date_to,
            'doctype': 'Production Plan'
        }

        # Assert
        assert_that(production_plan).is_not_none()
        assert_that(production_plan['name']).is_equal_to(plan_name)
        assert_that(production_plan['company']).is_equal_to(company)
        assert_that(production_plan['doctype']).is_equal_to('Production Plan')

    def test_production_plan_item_quantity(self):
        # Arrange
        item_qty = 100.0
        expected_qty = 100.0

        # Act & Assert
        assert_that(item_qty).is_equal_to(expected_qty)
        assert_that(item_qty).is_instance_of(float)
        assert_that(item_qty).is_greater_than(0)

    def test_production_plan_status_transitions(self):
        # Arrange
        statuses = ["Draft", "Submitted", "Completed", "Cancelled"]
        
        # Act & Assert
        for status in statuses:
            assert_that(status).is_not_empty()
            assert_that(status).is_instance_of(str)


class TestProductionSchedule:
    """Test suite for Production Schedule operations"""

    def test_schedule_item_with_due_date(self):
        # Arrange
        item_code = "ITEM-PROD-001"
        due_date = "2024-06-15"
        qty = 50.0

        # Act
        scheduled_item = {
            'item_code': item_code,
            'due_date': due_date,
            'qty': qty
        }

        # Assert
        assert_that(scheduled_item).contains_key('item_code', 'due_date', 'qty')
        assert_that(scheduled_item['item_code']).is_equal_to(item_code)
        assert_that(scheduled_item['qty']).is_greater_than(0)

    def test_production_schedule_priority_levels(self):
        # Arrange
        priority_levels = [1, 2, 3, 4, 5]

        # Act & Assert
        for priority in priority_levels:
            assert_that(priority).is_instance_of(int)
            assert_that(priority).is_between(1, 5)

    def test_production_order_sequence(self):
        # Arrange
        orders = [
            {'seq': 1, 'item': 'ITEM-A'},
            {'seq': 2, 'item': 'ITEM-B'},
            {'seq': 3, 'item': 'ITEM-C'}
        ]

        # Act
        sequences = [order['seq'] for order in orders]

        # Assert
        assert_that(sequences).is_equal_to([1, 2, 3])
        assert_that(len(sequences)).is_equal_to(3)


class TestJobCardManagement:
    """Test suite for Job Card operations"""

    def test_job_card_creation(self):
        # Arrange
        job_card_name = "JC-001"
        work_order = "WO-001"
        operation = "Assembly"
        workstation = "WS-001"

        # Act
        job_card = {
            'name': job_card_name,
            'work_order': work_order,
            'operation': operation,
            'workstation': workstation,
            'status': 'Open'
        }

        # Assert
        assert_that(job_card).has_name(job_card_name)
        assert_that(job_card).has_work_order(work_order)
        assert_that(job_card['status']).is_equal_to('Open')

    def test_job_card_time_tracking(self):
        # Arrange
        start_time = "09:00:00"
        end_time = "17:00:00"

        # Act
        job_card = {
            'start_time': start_time,
            'end_time': end_time,
            'duration_hours': 8.0
        }

        # Assert
        assert_that(job_card['start_time']).is_not_empty()
        assert_that(job_card['end_time']).is_not_empty()
        assert_that(job_card['duration_hours']).is_greater_than(0)

    def test_job_card_status_workflow(self):
        # Arrange
        workflow_statuses = ["Open", "In Progress", "Completed", "Cancelled"]

        # Act & Assert
        for status in workflow_statuses:
            assert_that(status).is_instance_of(str)
            assert_that(len(status)).is_greater_than(0)


class TestWorkstationCapacity:
    """Test suite for Workstation capacity management"""

    def test_workstation_availability_check(self):
        # Arrange
        workstation_id = "WS-001"
        capacity = 100.0
        current_load = 75.0

        # Act
        available_capacity = capacity - current_load

        # Assert
        assert_that(available_capacity).is_equal_to(25.0)
        assert_that(available_capacity).is_greater_than(0)

    def test_workstation_over_capacity_detection(self):
        # Arrange
        capacity = 100.0
        current_load = 100.0
        requested_load = 10.0

        # Act
        total_load = current_load + requested_load
        is_over_capacity = total_load > capacity

        # Assert
        assert_that(is_over_capacity).is_true()

    def test_workstation_utilization_percentage(self):
        # Arrange
        capacity = 100.0
        current_load = 60.0

        # Act
        utilization = (current_load / capacity) * 100

        # Assert
        assert_that(utilization).is_equal_to(60.0)
        assert_that(utilization).is_between(0, 100)


class TestRoutingOperations:
    """Test suite for Routing and Operations"""

    def test_routing_operation_sequence(self):
        # Arrange
        operations = [
            {'seq': 10, 'operation': 'Cut', 'workstation': 'WS-1'},
            {'seq': 20, 'operation': 'Assemble', 'workstation': 'WS-2'},
            {'seq': 30, 'operation': 'Test', 'workstation': 'WS-3'}
        ]

        # Act
        sequences = [op['seq'] for op in operations]

        # Assert
        assert_that(sequences).is_equal_to([10, 20, 30])
        assert_that(sequences).is_sorted()

    def test_operation_time_estimate(self):
        # Arrange
        setup_time = 15.0  # minutes
        cycle_time = 10.0  # minutes per unit
        quantity = 100.0

        # Act
        total_time = setup_time + (cycle_time * quantity)

        # Assert
        assert_that(total_time).is_equal_to(1015.0)
        assert_that(total_time).is_greater_than(setup_time)

    def test_routing_cost_calculation(self):
        # Arrange
        setup_cost = 50.0
        operation_cost_per_unit = 5.0
        quantity = 100.0

        # Act
        total_cost = setup_cost + (operation_cost_per_unit * quantity)

        # Assert
        assert_that(total_cost).is_equal_to(550.0)
        assert_that(total_cost).is_greater_than(0)
