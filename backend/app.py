import os
import json
from flask import Flask, request, jsonify
from firebase_admin import credentials, firestore, initialize_app
from api.movie import get_movie_poster
from api.book import get_book_cover
from api.upload import validate_image
from api.canva import create_final_image
from dotenv import load_dotenv

# Load environment variables from the .env file (for local development)
load_dotenv()

app = Flask(__name__)

# Initialize Firestore within app.py
def initialize_firestore():
    # Get the Firestore credentials from the environment variable
    firebase_credentials = os.getenv("FIREBASE_CREDENTIALS")
    
    if not firebase_credentials:
        raise Exception("FIREBASE_CREDENTIALS environment variable not found")

    # Parse the JSON string into a dictionary
    firebase_credentials_dict = json.loads(firebase_credentials)

    # Initialize Firebase app with the parsed credentials
    cred = credentials.Certificate(firebase_credentials_dict)
    initialize_app(cred)

    # Return Firestore client
    return firestore.client()

# Initialize Firestore
db = initialize_firestore()

@app.route('/api/process', methods=['POST'])
def process_form():
    try:
        # Get user inputs from the request form
        movie = request.form.get('movie')
        book = request.form.get('book')
        file = request.files.get('file')

        # Ensure movie, book, and file are provided
        if not movie or not book or not file:
            return jsonify({'error': 'Missing movie, book, or file'}), 400

        # Get movie poster and book cover
        movie_poster = get_movie_poster(movie)
        book_cover = get_book_cover(book)

        if not movie_poster:
            return jsonify({'error': 'Could not fetch movie poster'}), 400

        if not book_cover:
            return jsonify({'error': 'Could not fetch book cover'}), 400

        # Validate and process the uploaded image
        if not validate_image(file):
            return jsonify({'error': 'Invalid image dimensions'}), 400

        # Create final image using Canva API or PIL
        final_image_url = create_final_image(movie_poster, book_cover, file)

        # Save user data to Firestore
        doc_ref = save_user_data(db, movie, book, final_image_url)

        # Return the final image URL and Firestore document ID
        return jsonify({'final_image': final_image_url, 'doc_id': doc_ref.id})

    except Exception as e:
        # Catch any unexpected errors
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Ensure environment variables are loaded (this would be unnecessary if deployed in Vercel)
    app.run(debug=True)