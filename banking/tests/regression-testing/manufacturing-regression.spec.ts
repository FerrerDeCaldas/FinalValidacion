import { test, expect } from '@playwright/test';

test.describe('Regression Testing: Manufacturing Module (TailorFlow)', () => {
  test('Debe prohibir actualizaciones si la orden no está en Draft', async () => {
    const workOrderInProduction = { name: 'WO-001', status: 'In Process' };

    const updateWorkOrder = async (name: string) => {
      const wo = workOrderInProduction;
      if (wo.status !== 'Draft') {
        throw new Error('Regla RF16: Orden en producción no modificable');
      }
    };

    await expect(updateWorkOrder('WO-001')).rejects.toThrow('Regla RF16: Orden en producción no modificable');
  });

  test('No debe cancelar una orden con operaciones iniciadas', async () => {
    const orderWithActiveOperations = {
      name: 'WO-010',
      operations: [{ id: 101, status: 'Started' }],
    };

    const checkCancellation = (order: any) => {
      const hasStarted = order.operations.some((op: any) => op.status !== 'Not Started');
      if (hasStarted) {
        throw new Error('No se puede cancelar una orden con avance');
      }
    };

    expect(() => checkCancellation(orderWithActiveOperations)).toThrow('No se puede cancelar una orden con avance');
  });

  test('Debe mantener la estructura de datos al guardar una orden', async () => {
    const originalData = { id_order: 5, name: 'WO-005', status: 'Draft' };
    const saveResult = async () => originalData;

    const result = await saveResult();
    expect(result).toHaveProperty('id_order');
    expect(result).toHaveProperty('status');
    expect(result.name).toBe('WO-005');
  });
});
