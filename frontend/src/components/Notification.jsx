export default function Notification({ notification }) {
  if (!notification) return null;

  const styles = {
    success: "bg-emerald-100 text-emerald-800 border-emerald-300",
    error: "bg-red-100 text-red-800 border-red-300",
    info: "bg-secondary text-foreground border-border",
  };

  return (
    <div className="w-full px-4">
      <div
        className={`max-w-7xl mx-auto mt-4 mb-2 border px-4 py-3 rounded-sm text-sm ${
          styles[notification.type]
        }`}
      >
        {notification.message}
      </div>
    </div>
  );
}
