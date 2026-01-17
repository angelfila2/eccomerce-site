import { useNotification } from "../context/NotificationContext";
import Notification from "../components/Notification";

export default function PublicLayout({ children }) {
  const { notification } = useNotification();

  return (
    <>
      <Notification notification={notification} />
      {children}
    </>
  );
}
