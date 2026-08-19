from fastapi import FastAPI
from typing import Optional
app = FastAPI()

products = [
    {"id": 1,"name": "Laptop","category": "Electronics","price": 75000},
    {"id": 2,"name": "Mobile Phone","category": "Electronics","price": 35000},
    {"id": 3,"name": "Tablet","category": "Electronics","price": 28000},
    {"id": 4,"name": "Office Chair","category": "Furniture","price": 12000},
    {"id": 5,"name": "Desk","category": "Furniture","price": 18000},
    {"id": 6,"name": "Keyboard","category": "Accessories","price": 2500},
    {"id": 7,"name": "Mouse","category": "Accessories","price": 1200},
    {"id": 8,"name": "Headphones","category": "Accessories","price": 4500},
    {"id": 9,"name": "Monitor","category": "Electronics","price": 22000},
    {"id": 10,"name": "Printer","category": "Electronics","price": 15000}
  ]

@app.get("/products")
def search_products(category: Optional[str] =  None,
                    max_price: Optional[int] =  None):
    filter_products = products
    if category:
        filter_products = [p for p in filter_products if p['category'].lower() == category.lower()]
    if max_price:
        filter_products = [p for p in filter_products if p['price'] >=  max_price]
    return filter_products
