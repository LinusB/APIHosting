from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class Recipe(BaseModel):
    name: str
    description: str
    duration: int
    tags: List[str]
    ingredients: List[str]

# class Product(BaseModel):
#     productId: str
#     productName: str
#     productQuantity: int
#     productMHD: str
#     kategorieId: str

# class ProductWithKategorieName(Product):
#     kategorieName: Optional[str] = None  # Wird beim Lesen ergänzt

class UserProduct(BaseModel):
    productId: str           # verweist auf products/{productId}
    quantity: int
    mhd: str

class UserProductWithDetails(UserProduct):
    productName: Optional[str]
    categoryName: Optional[str]

class User(BaseModel):
    createdAt: datetime
    email: str
    lastname: str
    name: str
    password: str

class Personalisation(BaseModel):
    Abnehmen: bool
    Gesundheit: bool
    Glutenunverträglichkeit: bool
    KeineEinschränkung: bool
    Laktoseintoleranz: bool
    Muskelaufbau: bool
    Nussallergie: bool
    Vegan: bool
    Vegetarisch: bool
