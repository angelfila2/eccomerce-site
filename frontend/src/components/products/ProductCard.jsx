import { Link } from "react-router-dom";

export default function ProductCard({ product }) {
  return (
    <Link
      to={`/products/${product.productId}`}
      className="border border-border bg-card hover:shadow-sm transition block"
    >
      {/* Image placeholder */}
      <div className="h-40 bg-muted flex items-center justify-center text-xs text-muted-foreground">
        Image not found
      </div>

      {/* Product info */}
      <div className="p-3 space-y-1">
        <div className="text-sm font-medium line-clamp-2">{product.name}</div>

        <div className="text-primary font-semibold">
          ${product.price.toFixed(2)}
        </div>
      </div>
    </Link>
  );
}
