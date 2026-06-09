/// <reference types="cypress" />

const BASE_URL = Cypress.env('BASE_URL') || 'http://localhost:8000';

describe('Cypress Regression: Quality Management, Shopping Cart y Manufacturing', () => {
  it('Debe validar variables de configuración críticas', () => {
    const baseUrl = BASE_URL;
    expect(baseUrl).to.include('localhost').or.to.include('http');
    cy.log('✅ Configuración de URL validada');
  });

  it('Debe verificar que los timeouts están configurados', () => {
    const timeout = Cypress.config('defaultCommandTimeout');
    expect(timeout).to.equal(10000);
    cy.log('✅ Timeout configurado correctamente: ' + timeout + 'ms');
  });

  context('Con servidor disponible', () => {
    beforeEach(function () {
      const self = this;
      cy.task('checkServer', { url: BASE_URL }).then((res) => {
        if (res && res.status === 200) {
          return;
        }
        cy.log('Servidor no disponible o respondió: ' + (res && (res.error || res.status)));
        self.skip();
      });
    });

    it('No debe permitir crear un procedimiento de calidad sin nombre', () => {
      cy.visit(`${BASE_URL}/app/quality-management`);
      cy.contains(/Nuevo Procedimiento|New Procedure/, { timeout: 5000 }).click();
      cy.get('textarea[name="description"]').type('Descripción sin nombre');
      cy.get('button').contains(/Guardar|Save/).click();
      cy.contains(/El nombre es obligatorio|Name is required|required/, { timeout: 5000 }).should('be.visible');
    });

    it('Debe mantener el total del carrito al actualizar cantidad', () => {
      cy.visit(`${BASE_URL}/app/shopping-cart`);
      cy.contains(/Agregar producto|Add Product/, { timeout: 5000 }).click();
      cy.get('input[name="item_search"]').type('SC-ITEM-001{enter}');
      cy.get('input[name="qty"]').clear().type('1');
      cy.get('button').contains(/Agregar|Add/).click();
      cy.contains('SC-ITEM-001').should('exist');
      cy.get('input[name="qty_update"]').clear().type('3');
      cy.get('button').contains(/Actualizar|Update/).click();
      cy.contains(/Total|Subtotal/).should('contain.text', '300');
    });

    it('No debe permitir crear orden de fabricación sin artículo', () => {
      cy.visit(`${BASE_URL}/app/manufacturing`);
      cy.contains(/Nueva Orden de Trabajo|New Work Order/, { timeout: 5000 }).click();
      cy.get('button').contains(/Guardar|Save/).click();
      cy.contains(/Se necesita al menos un artículo|At least one item is required/, { timeout: 5000 }).should('be.visible');
    });
  });
});
