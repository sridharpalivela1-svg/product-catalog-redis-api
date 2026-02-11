from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.schemas import ProductCreate, ProductResponse
from app.services.product_service import (
    create_product,
    get_product,
    update_product,
    delete_product,
)
from app.core.redis_client import redis_client
from app.core.config import settings
import json

router = APIRouter(prefix="/products", tags=["Products"])


@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create(product: ProductCreate, db: Session = Depends(get_db)):
    return create_product(db, product.name, product.description, product.price)


@router.get("/{product_id}", response_model=ProductResponse)
def retrieve(product_id: int, db: Session = Depends(get_db)):
    cache_key = f"product:{product_id}"

    # Cache hit
    if redis_client:
        try:
            cached_product = redis_client.get(cache_key)
            if cached_product:
                print("CACHE HIT")
                return json.loads(cached_product)
        except Exception as e:
            print("Redis error:", e)

    # Cache miss
    product = get_product(db, product_id)

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

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


@router.put("/{product_id}", response_model=ProductResponse)
def update(product_id: int, product: ProductCreate, db: Session = Depends(get_db)):

    updated = update_product(db, product_id, product.name, product.description, product.price)

    if not updated:
        raise HTTPException(status_code=404, detail="Product not found")

    # Invalidate cache
    if redis_client:
        try:
            redis_client.delete(f"product:{product_id}")
            print("CACHE INVALIDATED (UPDATE)")
        except Exception as e:
            print("Redis delete error:", e)

    return updated


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(product_id: int, db: Session = Depends(get_db)):

    deleted = delete_product(db, product_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Product not found")

    # Invalidate cache
    if redis_client:
        try:
            redis_client.delete(f"product:{product_id}")
            print("CACHE INVALIDATED (DELETE)")
        except Exception as e:
            print("Redis delete error:", e)

    return
