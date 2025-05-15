from firebase import db
from models import Recipe, User, Personalisation, UserProduct, UserProductWithDetails
from typing import List, Optional
from firebase_admin import firestore

def add_recipe(user_id: str, recipe: Recipe):
    doc_ref = db.collection("users").document(user_id).collection("Rezepte").document()
    doc_ref.set(recipe.dict())
    return doc_ref.id

def get_recipes(user_id: str) -> List[dict]:
    docs = db.collection("users").document(user_id).collection("Rezepte").stream()
    return [doc.to_dict() | {"id": doc.id} for doc in docs]

def delete_recipe(user_id: str, recipe_id: str):
    db.collection("users").document(user_id).collection("Rezepte").document(recipe_id).delete()
    return True

def update_recipe(uid: str, recipeId: str, updated_recipe: Recipe):
    ref = db.reference(f'{uid}/Rezepte/{recipeId}')
    ref.update(updated_recipe.dict())

# def add_product(uid: str, product: Product):
#     category_ref = db.collection("kategorie").document(product.kategorieId)
#     doc_ref = db.collection("users").document(uid).collection("Bestand").document(product.productId)
#     doc_ref.set({
#         "productId": product.productId,
#         "productName": product.productName,
#         "productQuantity": product.productQuantity,
#         "productMHD": product.productMHD,
#         "kategorie": category_ref  # Referenzobjekt speichern
#     })

# def get_products(uid: str) -> List[ProductWithKategorieName]:
#     docs = db.collection("users").document(uid).collection("Bestand").stream()
#     result = []
#     for doc in docs:
#         data = doc.to_dict()
#         if "kategorie" in data:
#             kategorie_ref = data["kategorie"]
#             kategorie_doc = kategorie_ref.get()
#             kategorie_data = kategorie_doc.to_dict() if kategorie_doc.exists else {}
#             kategorie_name = kategorie_data.get("name", "Unbekannt")
#             result.append(ProductWithKategorieName(
#                 productId=data["productId"],
#                 productName=data["productName"],
#                 productQuantity=data["productQuantity"],
#                 productMHD=data["productMHD"],
#                 kategorieId=kategorie_ref.id,
#                 kategorieName=kategorie_name
#             ))
#     return result

# def delete_product(uid: str, productId: str):
#     db.collection("users").document(uid).collection("Bestand").document(productId).delete()

# def update_product(uid: str, productId: str, updated_product: Product):
#     category_ref = db.collection("kategorie").document(updated_product.kategorieId)
#     db.collection("users").document(uid).collection("Bestand").document(productId).update({
#         "productName": updated_product.productName,
#         "productQuantity": updated_product.productQuantity,
#         "productMHD": updated_product.productMHD,
#         "kategorie": category_ref
#     })

# --- USERDATA: user_data/profile ---
def get_user(uid: str) -> Optional[dict]:
    docs = db.collection("users").document(uid).collection("userdata").stream()
    user_data = [doc.to_dict() | {"id": doc.id} for doc in docs]
    return user_data if user_data else None

def add_user(uid: str, user: User):
    db.collection("users").document(uid).collection("userdata").add(user.dict())

def update_user(uid: str, doc_id: str, user: User):
    db.collection("users").document(uid).collection("userdata").document(doc_id).update(user.dict())

def delete_user(uid: str, doc_id: str):
    db.collection("users").document(uid).collection("userdata").document(doc_id).delete()

# --- PERSONALISATION: personalisation/preferences ---
def set_personalisation(uid: str, data: Personalisation):
    db.collection("users").document(uid).collection("personalisation").add(data.dict())

def get_personalisation(uid: str) -> Optional[List[dict]]:
    docs = db.collection("users").document(uid).collection("personalisation").stream()
    personal_data = [doc.to_dict() | {"id": doc.id} for doc in docs]
    return personal_data if personal_data else None

def update_personalisation(uid: str, doc_id: str, data: Personalisation):
    db.collection("users").document(uid).collection("personalisation").document(doc_id).update(data.dict())

def delete_personalisation(uid: str, doc_id: str):
    db.collection("users").document(uid).collection("personalisation").document(doc_id).delete()

# Produkt dem Bestand eines Users hinzufügen
def add_user_product(uid: str, user_product: UserProduct):
    product_ref = db.collection("products").document(user_product.productId)
    data = {
        "productId": user_product.productId,
        "productRef": product_ref,
        "quantity": user_product.quantity,
        "mhd": user_product.mhd
    }
    db.collection("users").document(uid).collection("Bestand").add(data)

# Alle Bestandsprodukte eines Users inkl. Produktdetails lesen
def get_user_products(uid: str):
    docs = db.collection("users").document(uid).collection("Bestand").stream()
    results = []
    for doc in docs:
        data = doc.to_dict()
        if "productRef" in data:
            product_doc = data["productRef"].get()
            product_data = product_doc.to_dict() if product_doc.exists else {}
            product_name = product_data.get("name", "Unbekannt")
            category_ref = product_data.get("kategorie")
            category_name = None
            if category_ref:
                cat_doc = category_ref.get()
                category_name = cat_doc.to_dict().get("name", "Unbekannt") if cat_doc.exists else "Unbekannt"

            results.append(UserProductWithDetails(
                productId=data["productId"],
                quantity=data["quantity"],
                mhd=data["mhd"],
                productName=product_name,
                categoryName=category_name
            ))
    return results

# Produkt aus Bestand löschen
def delete_user_product(uid: str, doc_id: str):
    db.collection("users").document(uid).collection("Bestand").document(doc_id).delete()

# Produkt im Bestand updaten
def update_user_product(uid: str, doc_id: str, user_product: UserProduct):
    product_ref = db.collection("products").document(user_product.productId)
    db.collection("users").document(uid).collection("Bestand").document(doc_id).update({
        "productId": user_product.productId,
        "productRef": product_ref,
        "quantity": user_product.quantity,
        "mhd": user_product.mhd
    })

