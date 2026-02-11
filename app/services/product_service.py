from sqlalchemy.orm import Session
from app.models.product import Product


def create_product(db: Session, name: str, description: str, price: float):
    product = Product(name=name, description=description, price=price)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def get_product(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()


def update_product(db: Session, product_id: int, name: str, description: str, price: float):
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        return None

    product.name = name
    product.description = description
    product.price = price

    db.commit()
    db.refresh(product)

    return product


def delete_product(db: Session, product_id: int):
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        return False

    db.delete(product)
    db.commit()

    return True

