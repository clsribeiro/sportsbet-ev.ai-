import React from 'react';
import { useAuth } from '../context/AuthContext';
import NotificationToast from './NotificationToast';
import './Notification.css';

const NotificationContainer = () => {
  const { notifications } = useAuth();

  if (!Array.isArray(notifications)) {
    return null;
  }

  return (
    <div className="notification-container">
      {notifications.map(notification => (
        <NotificationToast
          key={notification.id}
          message={notification.message}
          type={notification.type}
        />
      ))}
    </div>
  );
};

export default NotificationContainer;
