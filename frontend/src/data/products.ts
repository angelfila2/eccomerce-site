import type { Product } from '../types'

export const products: Product[] = [
  {
    id: 'p_001', slug: 'arc-desk-lamp', name: 'Arc Desk Lamp', category: 'Workspace',
    description: 'A warm, dimmable light with a sculptural silhouette for focused evenings.',
    details: ['Three-stage touch dimmer', 'Warm 2700K LED', 'Powder-coated aluminium'],
    price: 129, inventory: 14, featured: true, accent: '#d8a15d',
    imageUrl: 'https://images.unsplash.com/photo-1507473885765-e6ed057f782c?auto=format&fit=crop&w=1200&q=85',
  },
  {
    id: 'p_002', slug: 'linen-throw', name: 'Washed Linen Throw', category: 'Living',
    description: 'Breathable European linen with a relaxed texture that gets softer over time.',
    details: ['100% European flax', 'Stone washed', '130 × 180 cm'],
    price: 94, inventory: 22, featured: true, accent: '#9c765f',
    imageUrl: 'https://images.unsplash.com/photo-1583845112203-454c2254ed87?auto=format&fit=crop&w=1200&q=85',
  },
  {
    id: 'p_003', slug: 'field-tote', name: 'Field Tote', category: 'Carry',
    description: 'A structured everyday tote in durable canvas with considered internal storage.',
    details: ['Waxed cotton canvas', 'Padded laptop sleeve', 'Vegetable-tanned handles'],
    price: 118, inventory: 9, featured: true, accent: '#596b58',
    imageUrl: 'https://images.unsplash.com/photo-1553062407-98eeb64c6a62?auto=format&fit=crop&w=1200&q=85',
  },
  {
    id: 'p_004', slug: 'stoneware-set', name: 'Everyday Stoneware', category: 'Living',
    description: 'Four hand-finished bowls with subtle variations that make every set unique.',
    details: ['Set of four', 'Dishwasher safe', 'Hand glazed in Portugal'],
    price: 76, inventory: 18, accent: '#8795a1',
    imageUrl: 'https://images.unsplash.com/photo-1610701596007-11502861dcfa?auto=format&fit=crop&w=1200&q=85',
  },
  {
    id: 'p_005', slug: 'focus-timer', name: 'Focus Timer', category: 'Workspace',
    description: 'A satisfyingly tactile timer for distraction-free work sessions.',
    details: ['Silent countdown', '60-minute range', 'Solid aluminium body'],
    price: 48, inventory: 31, accent: '#d05d46',
    imageUrl: 'https://images.unsplash.com/photo-1495364141860-b0d03eccd065?auto=format&fit=crop&w=1200&q=85',
  },
  {
    id: 'p_006', slug: 'cedar-incense', name: 'Cedar Incense', category: 'Wellness',
    description: 'A grounding blend of cedar, vetiver and quiet smoke for slower rituals.',
    details: ['40 sticks', 'Approximately 30 minutes each', 'Low-smoke formula'],
    price: 28, inventory: 40, accent: '#7b5f45',
    imageUrl: 'https://images.unsplash.com/photo-1603006905003-be475563bc59?auto=format&fit=crop&w=1200&q=85',
  },
  {
    id: 'p_007', slug: 'travel-flask', name: 'Travel Flask', category: 'Carry',
    description: 'A slim insulated flask that keeps its temperature without taking over your bag.',
    details: ['500 ml', '18-hour insulation', 'BPA-free'],
    price: 42, inventory: 26, accent: '#617b83',
    imageUrl: 'https://images.unsplash.com/photo-1602143407151-7111542de6e8?auto=format&fit=crop&w=1200&q=85',
  },
  {
    id: 'p_008', slug: 'rest-eye-mask', name: 'Silk Rest Mask', category: 'Wellness',
    description: 'A softly padded silk mask designed to block light without pressure.',
    details: ['22 momme silk', 'Adjustable band', 'Washable storage pouch'],
    price: 36, inventory: 15, accent: '#79708f',
    imageUrl: 'https://images.unsplash.com/photo-1616394584738-fc6e612e71b9?auto=format&fit=crop&w=1200&q=85',
  },
]

