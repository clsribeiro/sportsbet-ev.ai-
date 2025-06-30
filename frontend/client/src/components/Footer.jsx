import React from 'react';

const Footer = () => {
  const currentYear = new Date().getFullYear();

  return (
    <footer style={{
      padding: '2rem',
      marginTop: 'auto',
      backgroundColor: '#1a1a1a',
      borderTop: '1px solid #333',
      textAlign: 'center',
      color: '#888'
    }}>
      <p>&copy; {currentYear} SportsBet +EV AI. Todos os direitos reservados.</p>
      <p>As apostas devem ser feitas de forma responsável. Apenas para maiores de 18 anos.</p>
    </footer>
  );
};

export default Footer;
