import os
import json
from firebase_admin import credentials, firestore, initialize_app

# Firebase-Key aus Umgebungsvariable lesen
firebase_key = json.loads(os.environ["FIREBASE_KEY"])
cred = credentials.Certificate(firebase_key)

# Initialisieren
initialize_app(cred)
db = firestore.client()
