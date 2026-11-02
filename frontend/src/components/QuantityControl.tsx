import { Minus, Plus } from 'lucide-react'

export function QuantityControl({ value, max, onChange }: {
  value: number
  max: number
  onChange: (quantity: number) => void
}) {
  return (
    <div className="quantity-control" aria-label="Quantity">
      <button type="button" aria-label="Decrease quantity" onClick={() => onChange(value - 1)}><Minus size={15} /></button>
      <span>{value}</span>
      <button type="button" aria-label="Increase quantity" disabled={value >= max} onClick={() => onChange(value + 1)}><Plus size={15} /></button>
    </div>
  )
}

