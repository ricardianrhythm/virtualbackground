import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase App and Firestore DB
def initialize_firestore():
    # Replace 'path/to/firebase-key.json' with your actual Firebase credentials JSON file path
    cred = credentials.Certificate('path/to/firebase-key.json')
    firebase_admin.initialize_app(cred)
    return firestore.client()

# Save user data to Firestore
def save_user_data(db, movie, book, image_url):
    # Firestore document to store user submissions
    doc_ref = db.collection('user_submissions').add({
        'movie': movie,
        'book': book,
        'image_url': image_url
    })
    return doc_ref