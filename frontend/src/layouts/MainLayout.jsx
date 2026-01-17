import { useEffect } from "react";
import { useNavigate } from "react-router-dom";

import { useNotification } from "../context/NotificationContext";
import Notification from "../components/Notification";
import Header from "../components/Header";
import CategoryBar from "../components/CategoryBar";

export default function MainLayout({ children }) {
  const { notification } = useNotification();
  const navigate = useNavigate();

  useEffect(() => {
    function handler() {
      navigate("/login");
    }

    window.addEventListener("auth:redirect", handler);
    return () => window.removeEventListener("auth:redirect", handler);
  }, [navigate]);

  return (
    <>
      <Header />
      <CategoryBar />
      <Notification notification={notification} />
      {children}
    </>
  );
}
