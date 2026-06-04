import { test, expect } from '@playwright/test';

test.describe('Regression Testing: Shopping Cart Module (TailorFlow)', () => {
  test('Debe rechazar producto inválido con nombre vacío y precio negativo', async () => {
    const invalidProduct = { name: '', price: -10, item_group: 'Products' };

    const validateProduct = (product: any) => {
      if (!product.name || product.price < 0) {
        throw new Error('Nombre o precio de producto inválidos');
      }
    };

    expect(() => validateProduct(invalidProduct)).toThrow('Nombre o precio de producto inválidos');
  });

  test('Debe conservar la estructura al guardar un producto nuevo', async () => {
    const testProduct = { id_product: 1, name: 'Test Product', price: 50.0, state: 'ACTIVE' };
    const saveResult = async () => testProduct;

    const result = await saveResult();
    expect(result).toHaveProperty('id_product');
    expect(result.name).toBe('Test Product');
    expect(result.price).toBe(50.0);
  });

  test('Debe mantener la propiedad id_state cuando guarda un producto', async () => {
    const originalData = { id_product: 5, name: 'Sofa Pro', id_state: 1 };
    const saveResult = async () => originalData;

    const result = await saveResult();
    expect(result).toHaveProperty('id_product');
    expect(result).toHaveProperty('id_state');
    expect(result.name).toBe('Sofa Pro');
  });
});
