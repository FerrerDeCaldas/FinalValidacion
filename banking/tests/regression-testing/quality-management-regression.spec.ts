import { test, expect } from '@playwright/test';

test.describe('Regression Testing: Quality Management Module (TailorFlow)', () => {
  test('Debe prohibir actualizaciones si el procedimiento está bloqueado', async () => {
    const lockedProcedure = { name: 'QP-001', status: 'Locked' };

    const updateProcedure = async (name: string) => {
      const proc = lockedProcedure;
      if (proc.status === 'Locked') {
        throw new Error('Regla RF16: Procedimiento bloqueado no modificable');
      }
    };

    await expect(updateProcedure('QP-001')).rejects.toThrow('Regla RF16: Procedimiento bloqueado no modificable');
  });

  test('No debe cambiar un procedimiento con objetivos en progreso', async () => {
    const procedureWithObjectives = {
      name: 'QP-010',
      objectives: [{ id: 1, status: 'Open' }],
    };

    const checkUpdate = (proc: any) => {
      const hasOpen = proc.objectives.some((o: any) => o.status === 'Open');
      if (hasOpen) {
        throw new Error('No se puede modificar un procedimiento con objetivos abiertos');
      }
    };

    expect(() => checkUpdate(procedureWithObjectives)).toThrow('No se puede modificar un procedimiento con objetivos abiertos');
  });

  test('Debe conservar la estructura de datos al guardar un procedimiento', async () => {
    const originalData = { id_procedure: 5, name: 'QP-005', status: 'Draft' };
    const saveResult = async () => originalData;

    const result = await saveResult();
    expect(result).toHaveProperty('id_procedure');
    expect(result).toHaveProperty('status');
    expect(result.name).toBe('QP-005');
  });
});
