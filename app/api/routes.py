from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.schemas import ProductCreate, ProductResponse
from app.services.product_service import create_product, get_product
from app.core.redis_client import redis_client
from app.core.config import settings
import json

router = APIRouter(prefix="/products", tags=["Products"])


@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create(product: ProductCreate, db: Session = Depends(get_db)):
    new_product = create_product(db, product.name, product.description, product.price)
    return new_product


@router.get("/{product_id}", response_model=ProductResponse)
def retrieve(product_id: int, db: Session = Depends(get_db)):

    cache_key = f"product:{product_id}"

    # 1️⃣ Try cache first
    if redis_client:
        try:
            cached_product = redis_client.get(cache_key)
            if cached_product:
                print("CACHE HIT")
                return json.loads(cached_product)
        except Exception as e:
            print("Redis error:", e)

    # 2️⃣ Fetch from DB
    product = get_product(db, product_id)

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # 3️⃣ Store in cache
    if redis_client:
        try:
            redis_client.setex(
                cache_key,
                settings.CACHE_TTL,
                json.dumps({
                    "id": product.id,
                    "name": product.name,
                    "description": product.description,
                    "price": product.price
                })
            )
            print("CACHE MISS — Stored in Redis")
        except Exception as e:
            print("Redis error while setting:", e)

    return product

