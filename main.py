from fastapi import FastAPI, HTTPException, Query, Body
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from uuid import UUID, uuid4
from datetime import datetime

app = FastAPI()

class Product(BaseModel):
    id: UUID
    name: str
    description: Optional[str] = None
    price: float
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

products: List[Product] = []

@app.post("/products/", status_code=201, response_model=Product)
def create_product(product: Product):
    if any(p.id == product.id for p in products):
        raise HTTPException(status_code=400, detail="Produto com esse ID já existe")
    try:
        products.append(product)
        return product
    except Exception:
        raise HTTPException(status_code=500, detail="Erro ao inserir o produto")

@app.get("/products/", response_model=List[Product])
def list_products(
    min_price: Optional[float] = Query(None, description="Preço mínimo"),
    max_price: Optional[float] = Query(None, description="Preço máximo")
):
    filtered = products
    if min_price is not None:
        filtered = [p for p in filtered if p.price > min_price]
    if max_price is not None:
        filtered = [p for p in filtered if p.price < max_price]
    return filtered

@app.get("/products/{product_id}", response_model=Product)
def get_product(product_id: UUID):
    for product in products:
        if product.id == product_id:
            return product
    raise HTTPException(status_code=404, detail="Produto não encontrado")

@app.patch("/products/{product_id}", response_model=Product)
def patch_product(product_id: UUID, updated_fields: Dict[str, Any] = Body(...)):
    for i, product in enumerate(products):
        if product.id == product_id:
            update_data = updated_fields
            if 'updated_at' not in update_data:
                update_data['updated_at'] = datetime.utcnow()
            updated_product = product.copy(update=update_data)
            products[i] = updated_product
            return updated_product
    raise HTTPException(status_code=404, detail="Produto não encontrado")

@app.delete("/products/{product_id}", status_code=204)
def delete_product(product_id: UUID):
    for i, product in enumerate(products):
        if product.id == product_id:
            products.pop(i)
            return
    raise HTTPException(status_code=404, detail="Produto não encontrado")
