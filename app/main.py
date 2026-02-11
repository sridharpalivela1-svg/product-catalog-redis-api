from fastapi import FastAPI
from app.core.database import engine, Base
from app.api.routes import router

app = FastAPI(title="Product Catalog API")

Base.metadata.create_all(bind=engine)

app.include_router(router)


@app.get("/")
def root():
    return {"message": "Product Catalog API is running"}
