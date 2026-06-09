/// <reference types="cypress" />

const BASE_URL = Cypress.env('BASE_URL') || 'http://localhost:8000';

describe('Cypress Performance: Quality Management, Shopping Cart y Manufacturing', () => {
  it('Debe medir tiempo de respuesta de configuración', () => {
    const start = performance.now();
    const baseUrl = BASE_URL;
    const duration = performance.now() - start;
    expect(baseUrl).toBeTruthy();
    expect(duration).to.be.lessThan(10);
    cy.log(`✅ Acceso a configuración en ${duration.toFixed(2)}ms`);
  });

  it('Debe acceder a variables de ambiente eficientemente', () => {
    const start = performance.now();
    const user = Cypress.env('ERP_USER');
    const duration = performance.now() - start;
    expect(user).toBeDefined();
    expect(duration).to.be.lessThan(5);
    cy.log(`✅ Acceso a variables en ${duration.toFixed(2)}ms`);
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

    it('Debe cargar la página de Quality Management rápido', () => {
      const start = performance.now();
      cy.visit(`${BASE_URL}/app/quality-management`, { timeout: 10000 });
      cy.contains(/Procedimientos de Calidad|Quality Procedure/, { timeout: 5000 }).should('be.visible');
      cy.then(() => {
        const duration = performance.now() - start;
        cy.log(`⏱️ Quality Management cargado en ${duration.toFixed(2)}ms`);
        expect(duration).to.be.lessThan(5000);
      });
    });

    it('Debe abrir el dashboard de Shopping Cart en tiempo aceptable', () => {
      const start = performance.now();
      cy.visit(`${BASE_URL}/app/shopping-cart`, { timeout: 10000 });
      cy.contains(/Carrito|Shopping Cart/, { timeout: 5000 }).should('be.visible');
      cy.then(() => {
        const duration = performance.now() - start;
        cy.log(`⏱️ Shopping Cart cargado en ${duration.toFixed(2)}ms`);
        expect(duration).to.be.lessThan(5000);
      });
    });

    it('Debe iniciar flujo de fabricación en tiempo aceptable', () => {
      const start = performance.now();
      cy.visit(`${BASE_URL}/app/manufacturing`, { timeout: 10000 });
      cy.contains(/Producción|Manufacturing/, { timeout: 5000 }).should('be.visible');
      cy.then(() => {
        const duration = performance.now() - start;
        cy.log(`⏱️ Manufacturing cargado en ${duration.toFixed(2)}ms`);
        expect(duration).to.be.lessThan(5000);
      });
    });
  });
});
