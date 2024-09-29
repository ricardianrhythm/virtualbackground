import os
import json
from firebase_admin import credentials, firestore, initialize_app
from api.movie import get_movie_poster
from api.book import get_book_cover
from api.upload import validate_image
from api.canva import create_final_image

# Initialize Firestore within the serverless function
def initialize_firestore():
    firebase_credentials = os.getenv("FIREBASE_CREDENTIALS")
    if not firebase_credentials:
        raise Exception("FIREBASE_CREDENTIALS environment variable not found")

    firebase_credentials_dict = json.loads(firebase_credentials)

    # Initialize Firebase app with the parsed credentials
    cred = credentials.Certificate(firebase_credentials_dict)
    initialize_app(cred)

    # Return Firestore client
    return firestore.client()

# Initialize Firestore only once
db = initialize_firestore()

def handler(request):
    try:
        # Parse the incoming request data (Vercel sends requests as strings)
        if request.method == 'POST':
            # Ensure request body is JSON format
            if request.headers.get('content-type') == 'application/json':
                data = request.json
            else:
                data = request.form

            # Extract data from request
            movie = data.get('movie')
            book = data.get('book')
            file = request.files.get('file')

            # Ensure movie, book, and file are provided
            if not movie or not book or not file:
                return {
                    'statusCode': 400,
                    'body': json.dumps({'error': 'Missing movie, book, or file'})
                }

            # Get movie poster and book cover
            movie_poster = get_movie_poster(movie)
            book_cover = get_book_cover(book)

            if not movie_poster:
                return {
                    'statusCode': 400,
                    'body': json.dumps({'error': 'Could not fetch movie poster'})
                }

            if not book_cover:
                return {
                    'statusCode': 400,
                    'body': json.dumps({'error': 'Could not fetch book cover'})
                }

            # Validate and process the uploaded image
            if not validate_image(file):
                return {
                    'statusCode': 400,
                    'body': json.dumps({'error': 'Invalid image dimensions'})
                }

            # Create final image using Canva API or PIL
            final_image_url = create_final_image(movie_poster, book_cover, file)

            # Save user data to Firestore
            doc_ref = db.collection('user_submissions').add({
                'movie': movie,
                'book': book,
                'final_image_url': final_image_url
            })

            # Return the final image URL and Firestore document ID
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'final_image': final_image_url,
                    'doc_id': doc_ref.id
                })
            }
        else:
            return {
                'statusCode': 405,
                'body': json.dumps({'error': 'Method not allowed'})
            }

    except Exception as e:
        # Catch any unexpected errors and return an error response
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }