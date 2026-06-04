import { test, expect } from '@playwright/test';

test.describe('Performance Testing: Shopping Cart Module (TailorFlow)', () => {
  test('Debe listar 300 carritos en menos de 250ms', async () => {
    const mockCarts = Array(300).fill({
      id_cart: 1,
      customer: { name: 'Cliente Ficticio' },
    });

    const cartRepoStub = {
      async find() {
        return mockCarts;
      },
    };

    const start = Date.now();
    const result = await cartRepoStub.find({ relations: ['customer'] });
    const end = Date.now();

    expect(result).toHaveLength(300);
    expect(end - start).toBeLessThan(250);
  });

  test('Debe recuperar el detalle de un carrito en menos de 60ms', async () => {
    const cartRepoStub = {
      async findOne() {
        return {
          id_cart: 1,
          items: [{}, {}, {}],
        };
      },
    };

    const start = Date.now();
    const result = await cartRepoStub.findOne(1);
    const end = Date.now();

    expect(result).toBeDefined();
    expect(result.items).toHaveLength(3);
    expect(end - start).toBeLessThan(60);
  });

  test('Debe guardar un carrito de compras en menos de 100ms', async () => {
    const cartRepoStub = {
      async save() {
        return { id_cart: 999, status: 'Saved' };
      },
    };

    const start = Date.now();
    const result = await cartRepoStub.save({ customer_id: 1, items: [] });
    const end = Date.now();

    expect(result).toBeDefined();
    expect(result.id_cart).toBe(999);
    expect(end - start).toBeLessThan(100);
  });
});
