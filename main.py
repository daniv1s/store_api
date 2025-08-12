from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID, uuid4

app = FastAPI()

class Product(BaseModel):
    id: UUID
    name: str
    description: Optional[str] = None
    price: float

products = []

@app.post("/products/", status_code=201, response_model=Product)
def create_product(product: Product):
    products.append(product)
    return product

@app.get("/products/", response_model=List[Product])
def list_products():
    return products

@app.get("/products/{product_id}", response_model=Product)
def get_product(product_id: UUID):
    for product in products:
        if product.id == product_id:
            return product
    raise HTTPException(status_code=404, detail="Product not found")

@app.put("/products/{product_id}", response_model=Product)
def update_product(product_id: UUID, updated_product: Product):
    for i, product in enumerate(products):
        if product.id == product_id:
            products[i] = updated_product
            return updated_product
    raise HTTPException(status_code=404, detail="Product not found")

@app.delete("/products/{product_id}", status_code=204)
def delete_product(product_id: UUID):
    for i, product in enumerate(products):
        if product.id == product_id:
            products.pop(i)
            return
    raise HTTPException(status_code=404, detail="Product not found")
