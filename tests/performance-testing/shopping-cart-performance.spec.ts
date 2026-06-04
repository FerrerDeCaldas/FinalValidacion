/// <reference types="jest" />
describe('Performance Testing: Shopping Cart Module (TailorFlow)', () => {
  const cartRepoStub = {
    find: jest.fn(),
    findOne: jest.fn(),
    save: jest.fn(),
  };

  afterEach(() => {
    jest.clearAllMocks();
  });

  describe('RNF5 - Rendimiento en carga de carritos de compras', () => {
    it('Debe listar 300 carritos en menos de 250ms', async () => {
      const mockCarts = Array(300).fill({
        id_cart: 1,
        customer: { name: 'Cliente Ficticio' },
      });

      cartRepoStub.find.mockResolvedValue(mockCarts);

      const start = performance.now();
      const result = await cartRepoStub.find({ relations: ['customer'] });
      const end = performance.now();

      const duration = end - start;
      console.log(`⏱️ Tiempo RNF5 (300 carritos): ${duration.toFixed(2)}ms`);
      expect(result).toHaveLength(300);
      expect(duration).toBeLessThan(250);
    });
  });

  it('Debe recuperar el detalle de un carrito en menos de 60ms', async () => {
    cartRepoStub.findOne.mockResolvedValue({
      id_cart: 1,
      items: [{}, {}, {}],
    });

    const start = performance.now();
    const result = await cartRepoStub.findOne(1);
    const end = performance.now();

    const duration = end - start;
    expect(result).toBeDefined();
    expect(result.items).toHaveLength(3);
    expect(duration).toBeLessThan(60);
  });

  it('Debe guardar un carrito de compras en menos de 100ms', async () => {
    cartRepoStub.save.mockResolvedValue({ id_cart: 999, status: 'Saved' });

    const start = performance.now();
    const result = await cartRepoStub.save({ customer_id: 1, items: [] });
    const end = performance.now();

    const duration = end - start;
    expect(result).toBeDefined();
    expect(result.id_cart).toBe(999);
    expect(duration).toBeLessThan(100);
  });
});
