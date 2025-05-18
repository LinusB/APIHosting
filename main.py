from fastapi import FastAPI, HTTPException
from models import Recipe, User, Personalisation, UserProduct, UserProductWithDetails
from typing import List
from crud import (
    add_recipe, get_recipes, delete_recipe, update_recipe,
    add_user, get_user, update_user, delete_user,
    set_personalisation, get_personalisation, update_personalisation, delete_personalisation,
    add_user_product, get_user_products, update_user_product, delete_user_product
)

app = FastAPI()
print("main.py gestartet")


# @app.post("/users/{user_id}/recipes")
# def create_recipe(user_id: str, recipe: Recipe):
#     recipe_id = add_recipe(user_id, recipe)
#     return {"message": "Recipe created", "id": recipe_id}

# @app.get("/users/{user_id}/recipes")
# def read_recipes(user_id: str):
#     return get_recipes(user_id)

# @app.delete("/users/{user_id}/recipes/{recipe_id}")
# def remove_recipe(user_id: str, recipe_id: str):
#     delete_recipe(user_id, recipe_id)
#     return {"message": "Recipe deleted"}

# @app.put("/users/{uid}/recipes/{recipe_id}")
# def edit_recipe(uid: str, recipe_id: str, recipe: Recipe):
#     update_recipe(uid, recipe_id, recipe)
#     return {"message": "Recipe updated successfully"}

# @app.post("/users/{uid}/products/")
# def create_product(uid: str, product: Product):
#     add_product(uid, product)
#     return {"message": "Product added successfully"}

# @app.get("/users/{uid}/products/", response_model=List[ProductWithKategorieName])
# def read_products(uid: str):
#     return get_products(uid)

# @app.delete("/users/{uid}/products/{product_id}")
# def remove_product(uid: str, product_id: str):
#     delete_product(uid, product_id)
#     return {"message": "Product deleted successfully"}

# @app.put("/users/{uid}/products/{product_id}")
# def edit_product(uid: str, product_id: str, product: Product):
#     update_product(uid, product_id, product)
#     return {"message": "Product updated successfully"}

# --- USERDATA ---
# @app.get("/users/{uid}/userdata")
# def read_user(uid: str):
#     user = get_user(uid)
#     if user:
#         return user
#     raise HTTPException(status_code=404, detail="User not found")

# @app.post("/users/{uid}/userdata")
# def create_user(uid: str, user: User):
#     add_user(uid, user)
#     return {"message": "User profile created"}

# @app.put("/users/{uid}/userdata/{doc_id}")
# def edit_user(uid: str, doc_id: str, user: User):
#     update_user(uid, doc_id, user)
#     return {"message": "User profile updated"}

# @app.delete("/users/{uid}/userdata/{doc_id}")
# def remove_user(uid: str, doc_id: str):
#     delete_user(uid, doc_id)
#     return {"message": "User profile deleted"}

# --- PERSONALISATION ---
@app.post("/users/{uid}/personalisation")
def create_personalisation(uid: str, data: Personalisation):
    set_personalisation(uid, data)
    return {"message": "Personalisation saved"}

@app.get("/users/{uid}/personalisation")
def read_personalisation(uid: str):
    result = get_personalisation(uid)
    if result:
        return result
    raise HTTPException(status_code=404, detail="Personalisation not found")

@app.put("/users/{uid}/personalisation/{doc_id}")
def edit_personalisation(uid: str, doc_id: str, data: Personalisation):
    update_personalisation(uid, doc_id, data)
    return {"message": "Personalisation updated"}

@app.delete("/users/{uid}/personalisation/{doc_id}")
def remove_personalisation(uid: str, doc_id: str):
    delete_personalisation(uid, doc_id)
    return {"message": "Personalisation deleted"}

@app.post("/users/{uid}/bestand")
def create_user_product(uid: str, user_product: UserProduct):
    add_user_product(uid, user_product)
    return {"message": "Product added to user inventory"}

@app.get("/users/{uid}/bestand", response_model=List[UserProductWithDetails])
def read_user_products(uid: str):
    return get_user_products(uid)

@app.put("/users/{uid}/bestand/{doc_id}")
def edit_user_product(uid: str, doc_id: str, user_product: UserProduct):
    update_user_product(uid, doc_id, user_product)
    return {"message": "User product updated"}

@app.delete("/users/{uid}/bestand/{doc_id}")
def remove_user_product(uid: str, doc_id: str):
    delete_user_product(uid, doc_id)
    return {"message": "User product deleted"}

from datetime import datetime, timedelta
from fastapi import Query

@app.get("/users/{uid}/products/expiring")
def get_expiring_products(uid: str, days: int = Query(90, ge=1)):
    products = get_user_products(uid)
    now = datetime.now()
    future_date = now + timedelta(days=days)

    expiring_products = []

    for product in products:
        try:
            mhd_str = product.mhd
            if mhd_str:
                mhd_date = datetime.strptime(mhd_str, "%Y-%m-%d")
                if now <= mhd_date <= future_date:
                    expiring_products.append(product)
        except Exception as e:
            print(f"Fehler bei Produkt {product.productId}: {e}")

    return expiring_products
