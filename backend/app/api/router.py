from fastapi import APIRouter

from app.catalog.router import router as catalog_router
from app.orders.router import router as orders_router

api_router = APIRouter()
api_router.include_router(catalog_router)
api_router.include_router(orders_router)

# TODO(auth-last): Include app.accounts.router only after catalog, checkout,
# payments, operations and anonymous-order tests are complete.

