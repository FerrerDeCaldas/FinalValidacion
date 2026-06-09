/// <reference types="cypress" />

const BASE_URL = Cypress.env('BASE_URL') || 'http://localhost:8000';

describe('Cypress Security: Quality Management, Shopping Cart y Manufacturing', () => {
  it('Debe verificar que las credenciales están configuradas', () => {
    const user = Cypress.env('ERP_USER');
    const password = Cypress.env('ERP_PASSWORD');
    expect(user).toBeDefined();
    expect(password).toBeDefined();
    expect(user).to.not.be.empty;
    expect(password).to.not.be.empty;
    cy.log('✅ Credenciales configuradas correctamente');
  });

  it('Debe verificar que Web Security está desactivado para testing', () => {
    const webSecurity = Cypress.config('chromeWebSecurity');
    expect(webSecurity).to.equal(false);
    cy.log('✅ Web Security configurado para testing');
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

    it('Debe bloquear acceso anónimo a Quality Management', () => {
      cy.request({
        method: 'GET',
        url: `${BASE_URL}/api/resource/Quality Procedure`,
        failOnStatusCode: false,
      }).its('status').should('be.oneOf', [401, 403]);
    });

    it('Debe rechazar token inválido en el endpoint de Shopping Cart', () => {
      cy.request({
        method: 'GET',
        url: `${BASE_URL}/api/resource/Shopping Cart`,
        headers: {
          Authorization: 'Bearer invalid_token',
        },
        failOnStatusCode: false,
      }).its('status').should('be.oneOf', [401, 403]);
    });

    it('Debe permitir acceso autenticado y evitar SQL injection en Manufacturing', () => {
      cy.visit(`${BASE_URL}/login`);
      cy.get('input[name="usr"]').clear().type(Cypress.env('ERP_USER') || 'test@example.com');
      cy.get('input[name="pwd"]').clear().type(Cypress.env('ERP_PASSWORD') || 'Password123!');
      cy.get('button[type="submit"]').contains(/Iniciar sesión|Login|Sign in/).click();
      cy.url().should('not.include', '/login');

      cy.request({
        method: 'POST',
        url: `${BASE_URL}/api/resource/Work Order`,
        headers: {
          Authorization: `Bearer ${Cypress.env('ERP_TOKEN') || 'valid_token_placeholder'}`,
        },
        body: {
          item_code: "1' OR '1'='1",
          qty: 5,
        },
        failOnStatusCode: false,
      }).its('status').should('be.oneOf', [400, 422]);
    });
  });
});
