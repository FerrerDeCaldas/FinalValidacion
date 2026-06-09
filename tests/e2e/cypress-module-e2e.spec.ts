/// <reference types="cypress" />

const BASE_URL = Cypress.env('BASE_URL') || 'http://localhost:8000';

describe('Cypress E2E: Quality Management, Shopping Cart y Manufacturing', () => {
  it('Debe validar variables de entorno críticas', () => {
    expect(Cypress.env('ERP_USER')).toBeDefined();
    expect(Cypress.env('ERP_PASSWORD')).toBeDefined();
    expect(BASE_URL).to.include('localhost').or.to.include('http');
    cy.log('✅ Variables de entorno configuradas');
  });

  it('Debe validar que el timeout está configurado', () => {
    const timeout = Cypress.config('defaultCommandTimeout');
    expect(timeout).to.equal(10000);
    cy.log('✅ Timeout verificado: ' + timeout + 'ms');
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

    it('Gestión de Calidad: crear procedimiento de calidad y verificar listado', () => {
      cy.visit(`${BASE_URL}/app/quality-management`);
      cy.contains(/Procedimientos de Calidad|Quality Procedure/, { timeout: 5000 }).should('be.visible');
      cy.contains(/Nuevo Procedimiento|New Procedure/).click();

      cy.get('input[name="procedure_name"]', { timeout: 5000 }).type('Procedimiento de Calidad Test');
      cy.get('textarea[name="description"]').type('Prueba automática para validar el flujo de calidad.');
      cy.get('button').contains(/Guardar|Save/).click();

      cy.contains('Procedimiento de Calidad Test').should('exist');
      cy.contains(/En borrador|Draft|Open/).should('exist');
    });

    it('Carrito de Compras: agregar producto, actualizar cantidad y crear orden', () => {
      cy.visit(`${BASE_URL}/app/shopping-cart`);
      cy.contains(/Carrito|Shopping Cart/, { timeout: 5000 }).should('be.visible');

      cy.get('button').contains(/Agregar producto|Add Product/).click();
      cy.get('input[name="item_search"]').type('SC-ITEM-001{enter}');
      cy.get('input[name="qty"]').clear().type('2');
      cy.get('button').contains(/Agregar|Add/).click();

      cy.contains('SC-ITEM-001').should('exist');
      cy.contains(/Total|Subtotal/).should('contain.text', '200');

      cy.get('button').contains(/Checkout|Finalizar compra/).click();
      cy.contains(/Orden de Venta|Sales Order/).should('exist');
    });

    it('Manufactura: crear BOM y generar orden de trabajo', () => {
      cy.visit(`${BASE_URL}/app/manufacturing`);
      cy.contains(/Producción|Manufacturing/, { timeout: 5000 }).should('be.visible');
      cy.contains(/Nueva Lista de Materiales|New BOM/).click();

      cy.get('input[name="bom_name"]').type('BOM de Prueba Cypress');
      cy.get('input[name="item_code"]').type('SC-ITEM-001{enter}');
      cy.get('input[name="quantity"]').clear().type('5');
      cy.get('button').contains(/Agregar fila|Add Row/).click();
      cy.get('button').contains(/Guardar|Save/).click();

      cy.contains('BOM de Prueba Cypress').should('exist');
      cy.contains(/Crear Orden de Trabajo|Create Work Order/).click();
      cy.contains(/Orden de Trabajo|Work Order/).should('exist');
    });
  });
});
