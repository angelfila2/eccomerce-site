// src/context/NotificationContext.jsx
import { createContext, useContext, useRef, useState } from "react";

const NotificationContext = createContext(null);

export function NotificationProvider({ children }) {
  const [notification, setNotification] = useState(null);
  const timerRef = useRef(null);

  function show(message, type = "info") {
    if (timerRef.current) {
      clearTimeout(timerRef.current);
    }

    setNotification({ message, type });

    timerRef.current = setTimeout(() => {
      setNotification(null);
      timerRef.current = null;
    }, 10000);
  }

  return (
    <NotificationContext.Provider value={{ notification, show }}>
      {children}
    </NotificationContext.Provider>
  );
}

// ✅ THIS MUST EXIST
export function useNotification() {
  const ctx = useContext(NotificationContext);
  if (!ctx) {
    throw new Error("useNotification must be used inside NotificationProvider");
  }
  return ctx;
}
