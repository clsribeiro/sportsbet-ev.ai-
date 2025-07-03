import React, { useEffect, useState } from 'react';
import './Notification.css';

const NotificationToast = ({ message, type = 'info' }) => {
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    const enterTimeout = setTimeout(() => setVisible(true), 50);
    const exitTimeout = setTimeout(() => setVisible(false), 6500);
    return () => {
      clearTimeout(enterTimeout);
      clearTimeout(exitTimeout);
    };
  }, []);

  // Adiciona uma classe CSS com base no tipo da notificação
  const toastClass = `notification-toast ${visible ? 'show' : ''} toast-${type}`;

  return (
    <div className={toastClass}>
      <div className="notification-content">
        <strong>Alerta!</strong>
        <p>{message}</p>
      </div>
    </div>
  );
};

export default NotificationToast;
