/// <reference types="jest" />
describe('Regression Testing: Quality Management Module (TailorFlow)', () => {
  const qualityRepoStub = {
    preload: jest.fn(),
    save: jest.fn(),
  };

  afterEach(() => {
    jest.clearAllMocks();
  });

  describe('RF16 - Inmutabilidad del procedimiento en revisión', () => {
    it('Debe prohibir actualizaciones si el procedimiento está bloqueado', async () => {
      const lockedProcedure = { name: 'QP-001', status: 'Locked' };
      qualityRepoStub.preload.mockResolvedValue(lockedProcedure);

      const updateProcedure = async (name: string) => {
        const proc = await qualityRepoStub.preload(name);
        if (proc.status === 'Locked') {
          throw new Error('Regla RF16: Procedimiento bloqueado no modificable');
        }
      };

      await expect(updateProcedure('QP-001')).rejects.toThrow('Regla RF16: Procedimiento bloqueado no modificable');
    });
  });

  describe('RF17 - Integridad de revisión', () => {
    it('No debe cambiar un procedimiento con objetivos en progreso', () => {
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
  });

  describe('RNF18 - Consistencia de datos', () => {
    it('Debe conservar la estructura de datos al guardar un procedimiento', async () => {
      const originalData = { id_procedure: 5, name: 'QP-005', status: 'Draft' };
      qualityRepoStub.save.mockResolvedValue(originalData);

      const result = await qualityRepoStub.save(originalData);
      expect(result).toHaveProperty('id_procedure');
      expect(result).toHaveProperty('status');
      expect(result.name).toBe('QP-005');
    });
  });
});
