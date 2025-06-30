import React from 'react';
import { Outlet } from 'react-router-dom';
import Navbar from './Navbar';
import Footer from './Footer';

const MainLayout = () => {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
      <Navbar />
      <main style={{ flex: 1, padding: '2rem' }}>
        {/* O Outlet renderiza o conteúdo da rota filha (ex: Dashboard, PredictionsPage) */}
        <Outlet />
      </main>
      <Footer />
    </div>
  );
};

export default MainLayout;
