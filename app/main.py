from fastapi import FastAPI
from app.core.database import engine, Base
from app.models import product

app = FastAPI(title="Product Catalog API")

# Create tables automatically
Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"message": "Product Catalog API is running"}
