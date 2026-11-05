from fastapi import APIRouter

from app.catalog.router import router as catalog_router
from app.orders.router import router as orders_router
from app.accounts.router import router as accounts_router
from app.categories.router import router as categories_router
from app.cart.router import router as cart_router
from app.interactions.router import router as interactions_router
from app.recommendations.router import router as recommendations_router

api_router = APIRouter()
api_router.include_router(catalog_router)
api_router.include_router(orders_router)
api_router.include_router(accounts_router)
api_router.include_router(categories_router)
api_router.include_router(cart_router)
api_router.include_router(interactions_router)
api_router.include_router(recommendations_router)

# BE-008 owns account-router registration after validation and authorization pass.
# BE-001 is tested on a standalone router; BE-013 owns recommendation registration.
# Follow docs/learning/TASKS.md rather than the historical auth-last sequencing.

