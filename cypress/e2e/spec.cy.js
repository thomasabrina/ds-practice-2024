describe('Single Order Flow', () => {
  it('places a single non-fraudulent order', () => {
    cy.visit('/order-page'); // Adjust URL as needed
    cy.get('#book-id').type('123');
    cy.get('#submit-order').click();
    cy.get('.order-success').should('contain', 'Order placed successfully');
  });
});

describe('Multiple Orders Flow', () => {
  const orders = [{ bookId: '123' }, { bookId: '456' }, { bookId: '789' }];
  orders.forEach(order => {
    it(`places order for book ${order.bookId}`, () => {
      cy.visit('/order-page');
      cy.get('#book-id').type(order.bookId);
      cy.get('#submit-order').click();
      cy.get('.order-success').should('contain', 'Order placed successfully');
    });
  });
});

describe('Conflicting Orders Flow', () => {
  it('attempts to place conflicting orders', () => {
    cy.visit('/order-page');
    cy.get('#book-id').type('123');
    cy.get('#submit-order').click();
    cy.get('#book-id').clear().type('123'); // Same book in quick succession
    cy.get('#submit-order').click();
    cy.get('.order-error').should('contain', 'Order conflict detected');
  });
});