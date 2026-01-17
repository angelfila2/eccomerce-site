import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

import Header from "../../components/Header";
import CategoryBar from "../../components/CategoryBar";

import { getOrderById } from "../../api/orderApi";
import { useNotification } from "../../context/NotificationContext";

export default function OrderPage() {
  const { id } = useParams();
  const { show } = useNotification();

  const [order, setOrder] = useState(null);

  useEffect(() => {
    async function loadOrder() {
      try {
        const res = await getOrderById(id);
        setOrder(res.data);
      } catch (err) {
        show("Failed to load order :" + err, "error");
      }
    }
    loadOrder();
  }, [id]);

  function handlePay() {
    alert(
      "Thank You for using our services.\n\n" +
        "Payment gateway will soon be implemented.\n\n" +
        "If you have any feedback about this shopping demo,\n" +
        "feel free to contact me @angelfila2/github.\n\n" +
        "Thank you once again!"
    );
  }

  if (!order) return <div>Loading…</div>;

  return (
    <>
      <Header />
      <CategoryBar />

      <main className="max-w-4xl mx-auto p-6">
        <h1 className="text-xl font-semibold mb-6">Order #{order.id}</h1>

        <div className="space-y-4">
          {order.items.map((item) => (
            <div
              key={item.productId}
              className="flex justify-between border p-4"
            >
              <div>
                <div className="font-medium">{item.productName}</div>
                <div className="text-sm">
                  ${item.price} × {item.quantity}
                </div>
              </div>
              <div className="font-semibold">
                ${(item.price * item.quantity).toFixed(2)}
              </div>
            </div>
          ))}
        </div>

        <div className="mt-6 text-right">
          <div className="text-lg font-semibold mb-2">
            Total: ${order.totalAmount.toFixed(2)}
          </div>
          <button className="bg-primary px-6 py-2" onClick={handlePay}>
            Proceed to Pay
          </button>
        </div>
      </main>
    </>
  );
}
