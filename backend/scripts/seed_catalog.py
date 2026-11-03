"""Insert or update the starter catalog products."""

from decimal import Decimal

from sqlalchemy import select

from app.catalog.models import Category, Product
from app.db.session import SessionFactory
from app.inventory.models import Inventory


CATEGORIES = [
    {"name": "Living", "slug": "living"},
    {"name": "Workspace", "slug": "workspace"},
    {"name": "Carry", "slug": "carry"},
    {"name": "Wellness", "slug": "wellness"},
]

PRODUCTS = [
    {
        "slug": "arc-desk-lamp",
        "name": "Arc Desk Lamp",
        "category_slug": "workspace",
        "description": "A warm, dimmable light with a sculptural silhouette for focused evenings.",
        "details": [
            "Three-stage touch dimmer",
            "Warm 2700K LED",
            "Powder-coated aluminium",
        ],
        "price": Decimal("129.00"),
        "inventory": 14,
        "featured": True,
        "accent": "#d8a15d",
        "image_url": "https://images.unsplash.com/photo-1507473885765-e6ed057f782c?auto=format&fit=crop&w=1200&q=85",
    },
    {
        "slug": "linen-throw",
        "name": "Washed Linen Throw",
        "category_slug": "living",
        "description": "Breathable European linen with a relaxed texture that gets softer over time.",
        "details": ["100% European flax", "Stone washed", "130 × 180 cm"],
        "price": Decimal("94.00"),
        "inventory": 22,
        "featured": True,
        "accent": "#9c765f",
        "image_url": "https://images.unsplash.com/photo-1602810440890-82b4eb233d0b?auto=format&fit=crop&w=1200&q=85",
    },
    {
        "slug": "field-tote",
        "name": "Field Tote",
        "category_slug": "carry",
        "description": "A structured everyday tote in durable canvas with considered internal storage.",
        "details": [
            "Waxed cotton canvas",
            "Padded laptop sleeve",
            "Vegetable-tanned handles",
        ],
        "price": Decimal("118.00"),
        "inventory": 9,
        "featured": True,
        "accent": "#596b58",
        "image_url": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?auto=format&fit=crop&w=1200&q=85",
    },
    {
        "slug": "stoneware-set",
        "name": "Everyday Stoneware",
        "category_slug": "living",
        "description": "Four hand-finished bowls with subtle variations that make every set unique.",
        "details": ["Set of four", "Dishwasher safe", "Hand glazed in Portugal"],
        "price": Decimal("76.00"),
        "inventory": 18,
        "featured": False,
        "accent": "#8795a1",
        "image_url": "https://images.unsplash.com/photo-1610701596007-11502861dcfa?auto=format&fit=crop&w=1200&q=85",
    },
    {
        "slug": "focus-timer",
        "name": "Focus Timer",
        "category_slug": "workspace",
        "description": "A satisfyingly tactile timer for distraction-free work sessions.",
        "details": ["Silent countdown", "60-minute range", "Solid aluminium body"],
        "price": Decimal("48.00"),
        "inventory": 31,
        "featured": False,
        "accent": "#d05d46",
        "image_url": "https://images.unsplash.com/photo-1495364141860-b0d03eccd065?auto=format&fit=crop&w=1200&q=85",
    },
    {
        "slug": "cedar-incense",
        "name": "Cedar Incense",
        "category_slug": "wellness",
        "description": "A grounding blend of cedar, vetiver and quiet smoke for slower rituals.",
        "details": ["40 sticks", "Approximately 30 minutes each", "Low-smoke formula"],
        "price": Decimal("28.00"),
        "inventory": 40,
        "featured": False,
        "accent": "#7b5f45",
        "image_url": "https://images.unsplash.com/photo-1603006905003-be475563bc59?auto=format&fit=crop&w=1200&q=85",
    },
    {
        "slug": "travel-flask",
        "name": "Travel Flask",
        "category_slug": "carry",
        "description": "A slim insulated flask that keeps its temperature without taking over your bag.",
        "details": ["500 ml", "18-hour insulation", "BPA-free"],
        "price": Decimal("42.00"),
        "inventory": 26,
        "featured": False,
        "accent": "#617b83",
        "image_url": "https://images.unsplash.com/photo-1602143407151-7111542de6e8?auto=format&fit=crop&w=1200&q=85",
    },
    {
        "slug": "rest-eye-mask",
        "name": "Silk Rest Mask",
        "category_slug": "wellness",
        "description": "A softly padded silk mask designed to block light without pressure.",
        "details": ["22 momme silk", "Adjustable band", "Washable storage pouch"],
        "price": Decimal("36.00"),
        "inventory": 15,
        "featured": False,
        "accent": "#79708f",
        "image_url": "https://images.unsplash.com/photo-1616394584738-fc6e612e71b9?auto=format&fit=crop&w=1200&q=85",
    },
]


def seed_catalog() -> None:
    """Create missing records and update existing ones using their slugs."""
    with SessionFactory.begin() as session:
        categories_by_slug: dict[str, Category] = {}

        for category_data in CATEGORIES:
            category = session.scalar(
                select(Category).where(Category.slug == category_data["slug"])
            )

            if category is None:
                category = Category(**category_data)
                session.add(category)
            else:
                category.name = category_data["name"]

            categories_by_slug[category.slug] = category

        session.flush()

        for product_data in PRODUCTS:
            product = session.scalar(
                select(Product).where(Product.slug == product_data["slug"])
            )
            category = categories_by_slug[product_data["category_slug"]]
            quantity = product_data["inventory"]

            values = {
                key: value
                for key, value in product_data.items()
                if key not in {"category_slug", "inventory"}
            }

            if product is None:
                product = Product(**values, category=category, currency="SGD")
                product.inventory_record = Inventory(quantity=quantity)
                session.add(product)
            else:
                for field, value in values.items():
                    setattr(product, field, value)
                product.category = category
                product.currency = "SGD"

                if product.inventory_record is None:
                    product.inventory_record = Inventory(quantity=quantity)
                else:
                    product.inventory_record.quantity = quantity

    print(f"Catalog seeded: {len(CATEGORIES)} categories and {len(PRODUCTS)} products.")


if __name__ == "__main__":
    seed_catalog()
